#!/usr/bin/env python3
"""Local observation and correction panel for oratores runs.

The agents do not know this exists. They write JSON into a run directory; this
serves a view over whatever is there and writes back only two things: a decided
choice and a corrected assumption. Nothing here is required for the skill to
work — with the server off you still have the run directory and the artifact.

    python ui/server.py                 # http://127.0.0.1:8787
    python ui/server.py --port 9000 --root /path/to/oratores

Stdlib only. If `jsonschema` happens to be installed it is used to validate
what the agents wrote; if not, validation is skipped and said so.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import re
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

UI_DIR = Path(__file__).resolve().parent
REPO = UI_DIR.parent
SCHEMA = REPO / "skills" / "oratores" / "schema" / "run-artifacts.schema.json"

ARTIFACTS = [
    "agents.json",
    "brief.json",
    "evidence.json",
    "objections.json",
    "candidates.json",
    "choices.json",
    "assumptions.json",
    "findings.json",
]

DEF_FOR = {
    "agents.json": "manifest",
    "brief.json": "brief",
    "evidence.json": "evidence",
    "objections.json": "objections",
    "candidates.json": "candidates",
    "choices.json": "choices",
    "assumptions.json": "assumptions",
    "findings.json": "findings",
}

SAFE_ID = re.compile(r"^[A-Za-z0-9._-]+$")

try:
    import jsonschema  # type: ignore

    HAVE_SCHEMA = True
except Exception:  # pragma: no cover - optional
    HAVE_SCHEMA = False


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Store:
    """Reads a run directory. Holds no state beyond a write lock."""

    def __init__(self, runs_dir: Path) -> None:
        self.runs = runs_dir
        self.lock = threading.Lock()
        self.schema = None
        if HAVE_SCHEMA and SCHEMA.is_file():
            try:
                self.schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
            except Exception as exc:
                print(f"warn  could not load schema: {exc}")

    # -- reading -----------------------------------------------------------
    def run_dir(self, run_id: str) -> Path | None:
        if not SAFE_ID.match(run_id or ""):
            return None
        d = self.runs / run_id
        try:
            d.resolve().relative_to(self.runs.resolve())
        except ValueError:
            return None
        return d if d.is_dir() else None

    def list_runs(self) -> list[dict]:
        if not self.runs.is_dir():
            return []
        out = []
        for d in sorted(self.runs.iterdir(), reverse=True):
            if not d.is_dir():
                continue
            manifest = self._read(d / "agents.json") or {}
            out.append(
                {
                    "run_id": d.name,
                    "task": manifest.get("task", ""),
                    "mode": manifest.get("mode", ""),
                    "started": manifest.get("started"),
                    "finished": manifest.get("finished"),
                    "mtime": max(
                        [p.stat().st_mtime for p in d.glob("*") if p.is_file()] or [0]
                    ),
                }
            )
        return out

    def _read(self, path: Path):
        if not path.is_file():
            return None
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {"__error__": f"{path.name} is not valid JSON: {exc}"}

    def _validate(self, name: str, data) -> list[str]:
        if not (self.schema and isinstance(data, dict) and "__error__" not in data):
            return []
        key = DEF_FOR.get(name)
        if not key:
            return []
        sub = {"$ref": f"#/$defs/{key}", "$defs": self.schema["$defs"]}
        try:
            jsonschema.validate(data, sub)
        except jsonschema.ValidationError as exc:  # type: ignore
            where = "/".join(str(p) for p in exc.absolute_path) or "(root)"
            return [f"{name}: {where} — {exc.message}"]
        except Exception:
            return []
        return []

    def payload(self, run_id: str) -> dict | None:
        d = self.run_dir(run_id)
        if d is None:
            return None
        files, problems, stamps = {}, [], {}
        for name in ARTIFACTS:
            p = d / name
            data = self._read(p)
            files[name] = data
            if data is None:
                continue
            stamps[name] = p.stat().st_mtime
            if isinstance(data, dict) and "__error__" in data:
                problems.append(data["__error__"])
            else:
                problems.extend(self._validate(name, data))
        artifact = d / "artifact.md"
        return {
            "run_id": run_id,
            "files": files,
            "artifact": artifact.read_text(encoding="utf-8") if artifact.is_file() else None,
            "problems": problems,
            "schema_checked": bool(self.schema),
            "stamps": stamps,
            "fingerprint": self.fingerprint(run_id),
        }

    def fingerprint(self, run_id: str) -> str:
        d = self.run_dir(run_id)
        if d is None:
            return ""
        parts = []
        for p in sorted(d.glob("*")):
            if p.is_file():
                st = p.stat()
                parts.append(f"{p.name}:{int(st.st_mtime * 1000)}:{st.st_size}")
        return "|".join(parts)

    # -- the only two writes ----------------------------------------------
    def decide(self, run_id: str, choice_id: str, chose: str, note: str = "") -> dict:
        d = self.run_dir(run_id)
        if d is None:
            return {"ok": False, "error": "unknown run"}
        path = d / "choices.json"
        with self.lock:
            data = self._read(path) or {}
            if "__error__" in data:
                return {"ok": False, "error": data["__error__"]}
            open_list = data.get("open") or []
            decided = data.get("decided") or []
            hit = next((c for c in open_list if c.get("id") == choice_id), None)
            if hit is None:
                return {"ok": False, "error": f"no open choice {choice_id!r}"}
            labels = [o.get("label") for o in hit.get("options", [])]
            if chose not in labels:
                return {"ok": False, "error": f"{chose!r} is not an option of {choice_id}"}
            open_list = [c for c in open_list if c.get("id") != choice_id]
            decided.append(
                {
                    "id": choice_id,
                    "question": hit.get("question", ""),
                    "chose": chose,
                    "rejected": [l for l in labels if l != chose],
                    "by": "author",
                    "at": now(),
                    "note": note,
                }
            )
            data["open"], data["decided"] = open_list, decided
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return {"ok": True}

    def correct(self, run_id: str, assumption_id: str, corrected_to: str) -> dict:
        d = self.run_dir(run_id)
        if d is None:
            return {"ok": False, "error": "unknown run"}
        path = d / "assumptions.json"
        with self.lock:
            data = self._read(path) or {}
            if "__error__" in data:
                return {"ok": False, "error": data["__error__"]}
            items = data.get("assumptions") or []
            hit = next((a for a in items if a.get("id") == assumption_id), None)
            if hit is None:
                return {"ok": False, "error": f"no assumption {assumption_id!r}"}
            hit["corrected_to"] = corrected_to or None
            hit["corrected_at"] = now() if corrected_to else None
            data["assumptions"] = items
            path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        return {"ok": True}


class Handler(BaseHTTPRequestHandler):
    server_version = "oratores-ui"
    store: Store

    def log_message(self, fmt, *args):  # quieter
        if "/api/events" not in (self.path or ""):
            sys.stderr.write(f"  {self.command} {self.path}\n")

    # -- helpers -----------------------------------------------------------
    def _json(self, obj, code: int = 200) -> None:
        body = json.dumps(obj, ensure_ascii=False).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def _static(self, name: str) -> None:
        path = (UI_DIR / name).resolve()
        try:
            path.relative_to(UI_DIR)
        except ValueError:
            self.send_error(403)
            return
        if not path.is_file():
            self.send_error(404)
            return
        ctype = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
        if ctype.startswith("text/") or ctype.endswith(("javascript", "json")):
            ctype += "; charset=utf-8"
        body = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    # -- routing -----------------------------------------------------------
    def do_GET(self) -> None:
        u = urlparse(self.path)
        q = parse_qs(u.query)
        if u.path in ("/", "/index.html"):
            return self._static("index.html")
        if u.path in ("/app.js", "/style.css", "/mark.png", "/icon.png", "/icon-small.png", "/favicon.ico"):
            return self._static(u.path.lstrip("/"))
        if u.path == "/api/runs":
            return self._json({"runs": self.store.list_runs(), "schema_checked": bool(self.store.schema)})
        if u.path.startswith("/api/run/"):
            payload = self.store.payload(u.path[len("/api/run/"):])
            return self._json(payload) if payload else self._json({"error": "unknown run"}, 404)
        if u.path == "/api/events":
            return self._events((q.get("run") or [""])[0])
        self.send_error(404)

    def do_POST(self) -> None:
        u = urlparse(self.path)
        try:
            length = int(self.headers.get("Content-Length") or 0)
            body = json.loads(self.rfile.read(length) or b"{}")
        except Exception as exc:
            return self._json({"ok": False, "error": f"bad body: {exc}"}, 400)

        m = re.match(r"^/api/run/([A-Za-z0-9._-]+)/(decide|assumption)$", u.path)
        if not m:
            return self.send_error(404)
        run_id, action = m.group(1), m.group(2)
        if action == "decide":
            res = self.store.decide(
                run_id, str(body.get("id", "")), str(body.get("chose", "")), str(body.get("note", ""))
            )
        else:
            res = self.store.correct(
                run_id, str(body.get("id", "")), str(body.get("corrected_to", ""))
            )
        return self._json(res, 200 if res.get("ok") else 400)

    # -- server-sent events ------------------------------------------------
    def _events(self, run_id: str) -> None:
        if self.store.run_dir(run_id) is None:
            return self.send_error(404)
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "keep-alive")
        self.end_headers()
        last = None
        try:
            while True:
                fp = self.store.fingerprint(run_id)
                if fp != last:
                    last = fp
                    self.wfile.write(b"event: changed\ndata: {}\n\n")
                else:
                    self.wfile.write(b": ping\n\n")
                self.wfile.flush()
                time.sleep(1.0)
        except (BrokenPipeError, ConnectionResetError, OSError):
            return


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--port", type=int, default=8787)
    ap.add_argument("--host", default="127.0.0.1")
    ap.add_argument("--root", default=str(REPO), help="package root containing run/")
    args = ap.parse_args()

    runs = Path(args.root).expanduser().resolve() / "run"
    runs.mkdir(parents=True, exist_ok=True)
    Handler.store = Store(runs)

    print(f"oratores panel   http://{args.host}:{args.port}")
    print(f"watching         {runs}")
    print(f"schema checking  {'on' if HAVE_SCHEMA and SCHEMA.is_file() else 'off (pip install jsonschema to enable)'}")
    print("the skill does not need this running. ctrl-c to stop.\n")
    try:
        ThreadingHTTPServer((args.host, args.port), Handler).serve_forever()
    except KeyboardInterrupt:
        print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
