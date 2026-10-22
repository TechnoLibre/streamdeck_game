#!/usr/bin/env python3
# © 2026 TechnoLibre (http://www.technolibre.ca)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
"""Who the gallery answers, standard library only.

Its routes act on a plain GET: launching a game, deleting saves. A real
server runs on 127.0.0.1 at a free port, with XDG_DATA_HOME in a temporary
directory, and each request sets the Host and Sec-Fetch-Site headers a
browser or the GNOME extension would send.

    python3 -m unittest discover -s tests
"""

import http.client
import http.server
import json
import os
import tempfile
import threading
import unittest
from pathlib import Path
from unittest import mock

from test_saves import load

ROOT = Path(__file__).resolve().parent.parent


class TestGalleryAccess(unittest.TestCase):
    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        env = mock.patch.dict(os.environ, {"XDG_DATA_HOME": folder.name})
        env.start()
        self.addCleanup(env.stop)
        self.gallery = load("gallery_access", ROOT / "gallery_server.py")
        self.server = http.server.HTTPServer(
            ("127.0.0.1", 0), self.gallery.GameHandler
        )
        self.port = self.server.server_address[1]
        thread = threading.Thread(target=self.server.serve_forever)
        thread.start()
        self.addCleanup(thread.join)
        self.addCleanup(self.server.shutdown)
        self.addCleanup(self.server.server_close)

    def get(self, path, host=None, site=None, method="GET"):
        conn = http.client.HTTPConnection("127.0.0.1", self.port, timeout=10)
        self.addCleanup(conn.close)
        conn.putrequest(method, path, skip_host=True)
        if host is None:
            host = "localhost:%d" % self.port
        conn.putheader("Host", host)
        if site:
            conn.putheader("Sec-Fetch-Site", site)
        conn.endheaders()
        res = conn.getresponse()
        return res.status, dict(res.getheaders()), res.read()

    def test_the_extension_and_the_gallery_page_are_served(self):
        for host in ("localhost:%d" % self.port, "127.0.0.1:%d" % self.port):
            for site in (None, "same-origin", "none"):
                with self.subTest(host=host, site=site):
                    status, headers, body = self.get("/api/saves", host, site)
                    self.assertEqual(200, status)
                    self.assertEqual(0, json.loads(body)["count"])
                    self.assertNotIn("Access-Control-Allow-Origin", headers)

    def test_another_host_is_refused(self):
        """A page that rebound its own name to 127.0.0.1 sends its name."""
        for host in ("attacker.example:%d" % self.port, "localhost:1", ""):
            with self.subTest(host=host):
                status, _headers, body = self.get("/api/saves/clear-all", host)
                self.assertEqual(403, status)
                self.assertEqual("unknown Host", json.loads(body)["error"])

    def test_a_request_from_another_site_is_refused_before_acting(self):
        with mock.patch.object(self.gallery, "_kill_current_game") as kill:
            for site in ("cross-site", "same-site"):
                with self.subTest(site=site):
                    status, _headers, body = self.get("/stop", site=site)
                    self.assertEqual(403, status)
                    self.assertEqual(
                        "request from another site", json.loads(body)["error"]
                    )
            kill.assert_not_called()

    def test_a_link_opened_from_outside_the_browser_does_not_act(self):
        """xdg-open, a mail or a chat client opens a link with
        Sec-Fetch-Site: none: it may read, never act."""
        saves = Path(os.environ["XDG_DATA_HOME"], "erplibre-home/streamdeck/save")
        saves.mkdir(parents=True)
        (saves / "djscratch_state.json").write_text("{}")
        status, _headers, _body = self.get("/api/saves/clear-all", site="none")
        self.assertEqual(403, status)
        self.assertTrue((saves / "djscratch_state.json").exists())
        status, _headers, body = self.get("/api/saves", site="none")
        self.assertEqual((200, 1), (status, json.loads(body)["count"]))

    def test_the_page_opens_from_a_link_on_another_site(self):
        """Another site cannot read the page, and its own requests then
        come as same-origin; its /api/ routes stay closed to that site."""
        for site in ("cross-site", "same-site", "none", None):
            with self.subTest(site=site):
                status, _headers, body = self.get("/", site=site)
                self.assertEqual(200, status)
                self.assertIn(b"<html", body.lower())
        self.assertEqual(403, self.get("/api/games", site="cross-site")[0])

    def test_no_other_file_is_served(self):
        for path in ("/.git/config", "/gallery_server.py", "/tests/", "/save/"):
            for method in ("GET", "HEAD"):
                with self.subTest(path=path, method=method):
                    self.assertEqual(404, self.get(path, method=method)[0])

    def test_head_is_checked_too(self):
        status, _headers, _body = self.get(
            "/", host="attacker.example:%d" % self.port, method="HEAD"
        )
        self.assertEqual(403, status)
        self.assertEqual(200, self.get("/", method="HEAD")[0])

    def test_delete_takes_a_plain_file_name_only(self):
        saves = Path(os.environ["XDG_DATA_HOME"], "erplibre-home/streamdeck/save")
        saves.mkdir(parents=True)
        (saves / ".hidden").write_text("x")
        (saves / "rec_1.wav").write_text("x")
        for name in ("x/.hidden", ".hidden", "x/rec_1.wav"):
            with self.subTest(name=name):
                self.assertEqual(
                    404, self.get("/api/saves/delete/" + name)[0]
                )
        self.assertTrue((saves / ".hidden").exists())
        self.assertTrue((saves / "rec_1.wav").exists())
        self.assertEqual(200, self.get("/api/saves/delete/rec_1.wav")[0])
        self.assertFalse((saves / "rec_1.wav").exists())

    def test_main_listens_on_this_machine_only(self):
        with mock.patch.object(
            self.gallery, "_games_refusal", return_value=None
        ), mock.patch.object(
            self.gallery, "_scan_games", return_value=[]
        ), mock.patch.object(
            self.gallery.http.server, "HTTPServer"
        ) as server, mock.patch.object(self.gallery.webbrowser, "open"):
            server.return_value.__enter__.return_value.serve_forever.side_effect = (
                KeyboardInterrupt
            )
            self.gallery.main()
        self.assertEqual(
            ("127.0.0.1", self.gallery.PORT), server.call_args.args[0]
        )


if __name__ == "__main__":
    unittest.main()
