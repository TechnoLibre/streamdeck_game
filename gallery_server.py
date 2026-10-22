#!/usr/bin/env python3
# © 2026 TechnoLibre (http://www.technolibre.ca)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)

"""Local web server for the Stream Deck game gallery.

Serves index.html and handles /launch/<game_id> requests
to start games in a terminal. Kills previous game terminal
before opening a new one.

Usage: python gallery_server.py, under the venv that has requirements.txt;
inside ERPLibre, make streamdeck_gallery. Then open http://localhost:8042
"""

import argparse
import glob
import http.server
import json
import os
import shlex
import signal
import subprocess
import sys
import threading
import urllib.parse
import webbrowser

PORT = 8042
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# games_cli sits next to the gallery; a gallery loaded by its path, as the
# tests do, does not have SCRIPT_DIR on sys.path yet.
sys.path.insert(0, SCRIPT_DIR)
import games_cli  # noqa: E402
# Cloned by ERPLibre at script/stream_deck/games/, the games find its root
# three levels up. Without ERPLibre, neither file below exists: no GAMES
# setting refuses the games, and a game runs without a hand-over.
ERPLIBRE_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..", ".."))
# Hands the deck over from the ERPLibre Home service to a game, then back.
HANDOVER = os.path.join(
    ERPLIBRE_DIR, "script", "install", "erplibre_home_handover.sh"
)
SETTINGS_LIB = os.path.join(
    ERPLIBRE_DIR, "script", "install", "erplibre_home_settings.sh"
)


def _games_refusal():
    """None when the games may run; else the line that says why.

    Inside ERPLibre, the GAMES setting decides, read at each call through
    ERPLibre's settings library, the one make and the hand-over read: a
    change counts without restarting the gallery. A read that fails (bash
    missing, timeout) refuses too, like an unknown value, and the line names
    the failure. Without ERPLibre, there is no setting: None."""
    if not os.path.isfile(SETTINGS_LIB):
        return None
    try:
        fini = subprocess.run(
            [
                "bash",
                "-c",
                '. "$0" && { deck_games_enabled'
                " || { deck_games_message; exit 1; }; }",
                SETTINGS_LIB,
            ],
            capture_output=True,
            text=True,
            timeout=10,
        )
    except (OSError, subprocess.TimeoutExpired) as echec:
        raison = " ".join(str(echec).split())
        return f"cannot read the GAMES setting: {raison}"
    if fini.returncode == 0:
        return None
    return fini.stdout.strip() or fini.stderr.strip() or "games disabled"


# Game metadata cache (populated at startup)
_game_cache = []


def _scan_games():
    """Scan all game_*.py files and collect metadata via --meta."""
    games = []
    for filepath in sorted(glob.glob(os.path.join(SCRIPT_DIR, "game_*.py"))):
        game_id = os.path.basename(filepath).replace("game_", "").replace(
            ".py", ""
        )
        try:
            result = subprocess.run(
                [sys.executable, filepath, "--meta"],
                capture_output=True, text=True, timeout=5,
            )
            if result.returncode == 0 and result.stdout.strip():
                meta = json.loads(result.stdout.strip())
                meta["id"] = game_id
                # Check if game has save files; main() moved the old ones.
                save_dir = games_cli.save_path()
                if os.path.isdir(save_dir):
                    has_saves = any(
                        game_id in f for f in os.listdir(save_dir)
                    )
                    if has_saves:
                        meta["saves"] = True
                games.append(meta)
            else:
                print(f"  WARN: {game_id} --meta failed: {result.stderr[:80]}")
        except (subprocess.TimeoutExpired, json.JSONDecodeError, Exception) as e:
            print(f"  WARN: {game_id}: {e}")
    return games

# Track the current game process
_current_game_proc = None


def _kill_current_game():
    """Kill the currently running game terminal if any."""
    global _current_game_proc
    if _current_game_proc is not None:
        try:
            # Send SIGTERM to the process group (terminal + children)
            pgid = os.getpgid(_current_game_proc.pid)
            os.killpg(pgid, signal.SIGTERM)
        except (ProcessLookupError, OSError):
            pass
        try:
            _current_game_proc.wait(timeout=2)
        except subprocess.TimeoutExpired:
            try:
                pgid = os.getpgid(_current_game_proc.pid)
                os.killpg(pgid, signal.SIGKILL)
            except (ProcessLookupError, OSError):
                pass
        _current_game_proc = None


def _exec_self():
    """Replace the current process with a fresh interpreter running
    the same script. Picks up edits without needing an external watcher."""
    try:
        os.execv(sys.executable, [sys.executable] + sys.argv)
    except Exception as e:
        print(f"execv failed: {e}", file=sys.stderr)


def _game_bash_cmd(game_file):
    """Return the bash command that runs game_file in a terminal.

    The game runs under sys.executable, the interpreter of this server, so
    it gets the server's venv instead of the python its shebang finds on
    PATH. Every path is quoted for bash. The loop restarts the game when the
    user types "r" + Enter at the end-of-game prompt, which avoids
    re-picking it from the gallery; any other answer, or a closed stdin,
    ends it. Inside ERPLibre, the whole loop runs inside one
    erplibre_home_handover.sh: the deck service stops before the first game
    and comes back once, when the loop ends, not between two rounds. Without
    ERPLibre, the loop runs on its own, from the games' directory.
    """
    loop = (
        f"while true; do "
        f"{shlex.quote(sys.executable)} {shlex.quote(game_file)}; "
        f'echo ""; '
        f'echo "Game ended. Press [r]+enter to restart, '
        f'or enter to close..."; '
        f"read -r ans; "
        f'if [ "$ans" != "r" ] && [ "$ans" != "R" ]; then break; fi; '
        f"done"
    )
    if not os.path.isfile(HANDOVER):
        return f"cd {shlex.quote(SCRIPT_DIR)} && bash -c {shlex.quote(loop)}"
    return (
        f"cd {shlex.quote(ERPLIBRE_DIR)} && "
        f"{shlex.quote(HANDOVER)} bash -c {shlex.quote(loop)}"
    )


class GameHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=SCRIPT_DIR, **kwargs)

    # The routes that act. Only the gallery page, by a same-origin fetch,
    # or a client that is not a browser (no Sec-Fetch-Site) reaches them:
    # a link opened from outside the browser comes as "none".
    ACTIONS = (
        "/launch/",
        "/stop",
        "/api/saves/delete/",
        "/api/saves/clear-game/",
        "/api/saves/clear-all",
        "/api/restart",
    )
    # The only files served: the page, self-contained.
    PAGES = ("/", "/index.html")

    def _refusal(self):
        """None for a request the gallery serves; else (status, why).

        Its routes act on a plain GET (launch a game, delete saves), so a
        request is served only from this machine, under its own name: a
        Host other than localhost or 127.0.0.1 at the gallery's port is a
        page that rebound its own name to this address. A browser marks
        the request any other page sends, even one it cannot read the
        answer of, with Sec-Fetch-Site: an action takes only same-origin
        or no header, the read-only /api/ routes also none (an address
        typed or opened by the desktop), and the page any, since another
        site cannot read it. Other paths are 404: nothing else is served."""
        port = self.server.server_address[1]
        if self.headers.get("Host", "") not in (
            "localhost:%d" % port,
            "127.0.0.1:%d" % port,
        ):
            return 403, "unknown Host"
        path = urllib.parse.urlsplit(self.path).path
        site = self.headers.get("Sec-Fetch-Site")
        if path.startswith(self.ACTIONS):
            if site not in (None, "same-origin"):
                return 403, "request from another site"
        elif path.startswith("/api/"):
            if site not in (None, "same-origin", "none"):
                return 403, "request from another site"
        elif path not in self.PAGES:
            return 404, "not found"
        return None

    def do_HEAD(self):
        refusal = self._refusal()
        if refusal:
            self.send_response(refusal[0])
            self.end_headers()
            return
        super().do_HEAD()

    def do_GET(self):
        refusal = self._refusal()
        if refusal:
            self._json_response({"error": refusal[1]}, refusal[0])
            return
        if self.path == "/api/games":
            self._json_response(_game_cache)
            return
        if self.path.startswith("/launch/"):
            game_id = self.path.split("/launch/")[1].strip("/")
            self._launch_game(game_id)
            return
        if self.path == "/stop":
            self._stop_game()
            return
        if self.path == "/api/saves":
            self._list_saves()
            return
        if self.path.startswith("/api/saves/delete/"):
            filename = self.path.split("/api/saves/delete/")[1].strip("/")
            self._delete_save(filename)
            return
        if self.path.startswith("/api/saves/clear-game/"):
            game_id = self.path.split("/api/saves/clear-game/")[1].strip("/")
            self._clear_game_saves(game_id)
            return
        if self.path == "/api/saves/clear-all":
            self._clear_all_saves()
            return
        if self.path == "/api/restart":
            self._restart_self()
            return
        super().do_GET()

    def _json_response(self, data, status=200):
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _list_saves(self):
        """List the files of the save directory, games_cli.save_dir()."""
        save_dir = games_cli.save_dir()
        files = []
        if os.path.isdir(save_dir):
            for f in sorted(os.listdir(save_dir)):
                if f.startswith("."):
                    continue
                path = os.path.join(save_dir, f)
                size = os.path.getsize(path)
                mtime = os.path.getmtime(path)
                ftype = "json" if f.endswith(".json") else "wav" if f.endswith(".wav") else "other"
                game = "djscratch" if "djscratch" in f or f.startswith("rec_") or f.startswith("sample_") or f.startswith("_mic") else "unknown"
                files.append({
                    "name": f,
                    "size": size,
                    "mtime": mtime,
                    "type": ftype,
                    "game": game,
                })
        total_size = sum(f["size"] for f in files)
        self._json_response({
            "files": files,
            "count": len(files),
            "total_size": total_size,
        })

    def _delete_save(self, filename):
        """Delete one save file, named by itself: a name with a directory
        part, or a dotfile, which the list and the clear routes skip, is
        not found."""
        save_dir = games_cli.save_dir()
        name = os.path.basename(filename)
        path = os.path.join(save_dir, name)
        if name == filename and not name.startswith(".") and os.path.isfile(path):
            os.remove(path)
            print(f"Deleted: {path}")
            self._json_response({"ok": True, "deleted": filename})
        else:
            self._json_response({"error": "File not found"}, 404)

    def _match_game(self, filename, game_id):
        """Check if a save file belongs to a game."""
        patterns = {
            "djscratch": [
                "djscratch", "rec_", "sample_", "_mic",
            ],
        }
        pats = patterns.get(game_id, [game_id])
        for p in pats:
            if p in filename:
                return True
        return False

    def _clear_game_saves(self, game_id):
        """Delete all save files for a specific game."""
        save_dir = games_cli.save_dir()
        count = 0
        if os.path.isdir(save_dir):
            for f in os.listdir(save_dir):
                if f.startswith("."):
                    continue
                if self._match_game(f, game_id):
                    path = os.path.join(save_dir, f)
                    if os.path.isfile(path):
                        os.remove(path)
                        count += 1
        print(f"Cleared {count} files for game: {game_id}")
        self._json_response({"ok": True, "deleted_count": count, "game": game_id})

    def _clear_all_saves(self):
        """Delete all save files."""
        save_dir = games_cli.save_dir()
        count = 0
        if os.path.isdir(save_dir):
            for f in os.listdir(save_dir):
                if f.startswith("."):
                    continue
                path = os.path.join(save_dir, f)
                if os.path.isfile(path):
                    os.remove(path)
                    count += 1
        print(f"Cleared {count} save files")
        self._json_response({"ok": True, "deleted_count": count})

    def _stop_game(self):
        """Stop the current game."""
        _kill_current_game()
        self._json_response({"ok": True})

    def _restart_self(self):
        """Reply OK then re-exec this server so source edits take effect."""
        self._json_response({"ok": True})
        try:
            self.wfile.flush()
        except Exception:
            pass
        _kill_current_game()
        # Defer execv so the response actually leaves the socket.
        threading.Timer(0.3, _exec_self).start()

    def _launch_game(self, game_id):
        global _current_game_proc

        refus = _games_refusal()
        if refus:
            self.send_response(403)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": refus}).encode())
            return

        game_file = os.path.join(SCRIPT_DIR, f"game_{game_id}.py")
        if not os.path.isfile(game_file):
            self.send_response(404)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(
                json.dumps({"error": f"Game not found: {game_id}"}).encode()
            )
            return

        # Kill previous game first
        _kill_current_game()

        print(f"Launching game: {game_id}")
        bash_cmd = _game_bash_cmd(game_file)
        try:
            # --wait keeps gnome-terminal process alive until window closes
            _current_game_proc = subprocess.Popen(
                [
                    "gnome-terminal", "--wait", "--",
                    "bash", "-c", bash_cmd,
                ],
                preexec_fn=os.setsid,
            )
            status = {"ok": True, "game": game_id}
        except FileNotFoundError:
            try:
                _current_game_proc = subprocess.Popen(
                    ["xterm", "-e", bash_cmd],
                    preexec_fn=os.setsid,
                )
                status = {"ok": True, "game": game_id}
            except FileNotFoundError:
                status = {
                    "error": "No terminal found (tried gnome-terminal, xterm)"
                }

        # 503 when no terminal could start: a 2xx means the game started.
        self.send_response(503 if "error" in status else 200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(status).encode())

    def log_message(self, format, *args):
        if "/launch/" in str(args) or "/stop" in str(args):
            super().log_message(format, *args)


def parser():
    """The command line. argparse exits 0 on -h and 2 on any argument it
    does not know, before main() scans the games, listens on PORT or opens
    a browser."""
    return argparse.ArgumentParser(
        description=(
            "Stream Deck game gallery.\n"
            "Without an option, it serves the gallery on"
            f" http://localhost:{PORT},\nopens it in the browser and"
            " launches the game picked there."
        ),
        epilog=(
            "Exit codes:\n"
            "  0  stopped by Ctrl+C, or --help\n"
            "  1  the port is taken, an unexpected error, or, inside"
            " ERPLibre,\n     GAMES is not on in erplibre-home/streamdeck.conf\n"
            "  2  a bad option"
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )


def main():
    global _game_cache
    refus = _games_refusal()
    if refus:
        print(refus, file=sys.stderr)
        sys.exit(1)
    # Moves the saves of the former save/ before the scan reads them.
    games_cli.save_dir()
    print("Scanning games...")
    _game_cache = _scan_games()
    print(f"Found {len(_game_cache)} games")

    handler = GameHandler
    # This machine only: the routes act on a plain GET.
    with http.server.HTTPServer(("127.0.0.1", PORT), handler) as httpd:
        url = f"http://localhost:{PORT}"
        print(f"Stream Deck Game Gallery: {url}")
        print("Press Ctrl+C to stop.")
        webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass
        _kill_current_game()
        print("\nServer stopped.")


if __name__ == "__main__":
    parser().parse_args()
    main()
