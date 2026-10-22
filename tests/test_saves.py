#!/usr/bin/env python3
# © 2026 TechnoLibre (http://www.technolibre.ca)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
"""The saves, outside the repository, standard library only.

games_cli and the gallery are copied into a temporary directory, so the
former save/ next to them and XDG_DATA_HOME are the test's own; nothing
reads or writes the real ones.

    python3 -m unittest discover -s tests
"""

import importlib.util
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Copy(unittest.TestCase):
    """games_cli.py and gallery_server.py at <tmp>/a/b/c/games/, with
    XDG_DATA_HOME at <tmp>/data."""

    def setUp(self):
        folder = tempfile.TemporaryDirectory()
        self.addCleanup(folder.cleanup)
        self.tmp = Path(folder.name)
        self.games = self.tmp / "a/b/c/games"
        self.games.mkdir(parents=True)
        for name in ("games_cli.py", "gallery_server.py"):
            shutil.copy(ROOT / name, self.games / name)
        self.data = self.tmp / "data"
        env = mock.patch.dict(os.environ, {"XDG_DATA_HOME": str(self.data)})
        env.start()
        self.addCleanup(env.stop)
        self.saves = self.data / "erplibre-home/streamdeck/save"
        self.cli = load("games_cli_copy", self.games / "games_cli.py")

    def legacy(self, files):
        old = self.games / "save"
        old.mkdir(exist_ok=True)
        for name, text in files.items():
            (old / name).write_text(text)
        return old


class TestSaveDirectory(Copy):
    def test_the_path_follows_xdg_data_home_and_creates_nothing(self):
        self.assertEqual(str(self.saves), self.cli.save_path())
        self.assertFalse(self.data.exists())
        home = self.tmp / "home"
        for value in ("", "relative/dir"):
            with self.subTest(xdg=value), mock.patch.dict(
                os.environ, {"XDG_DATA_HOME": value, "HOME": str(home)}
            ):
                self.assertEqual(
                    str(home / ".local/share/erplibre-home/streamdeck/save"),
                    self.cli.save_path(),
                )

    def test_save_dir_creates_it_and_moves_the_former_saves(self):
        old = self.legacy(
            {"djscratch_state.json": "{}", "rec_1.wav": "w", ".gitkeep": ""}
        )
        self.assertEqual(str(self.saves), self.cli.save_dir())
        self.assertEqual(
            ["djscratch_state.json", "rec_1.wav"],
            sorted(os.listdir(self.saves)),
        )
        self.assertEqual("{}", (self.saves / "djscratch_state.json").read_text())
        self.assertEqual([".gitkeep"], os.listdir(old))
        # A second call has nothing left to move.
        self.cli.save_dir()
        self.assertEqual(2, len(os.listdir(self.saves)))

    def test_a_save_already_there_is_never_replaced(self):
        self.saves.mkdir(parents=True)
        (self.saves / "rec_1.wav").write_text("new")
        old = self.legacy({"rec_1.wav": "old"})
        self.cli.save_dir()
        self.assertEqual("new", (self.saves / "rec_1.wav").read_text())
        self.assertEqual("old", (old / "rec_1.wav").read_text())

    def cross_filesystem_link(self):
        """os.link as across filesystems from the former save/: EXDEV for
        a link out of it, the real link inside the save directory."""
        real = os.link
        old = str(self.games / "save")

        def link(source, target):
            if str(source).startswith(old):
                raise OSError(18, "EXDEV")
            return real(source, target)

        return mock.patch.object(self.cli.os, "link", side_effect=link)

    def test_across_filesystems_the_copy_does_not_replace_either(self):
        """The copy takes over from the link, and still refuses a file
        already there."""
        old = self.legacy({"a.json": "1", "b.json": "2"})
        self.saves.mkdir(parents=True)
        (self.saves / "b.json").write_text("kept")
        with self.cross_filesystem_link():
            self.cli.save_dir()
        self.assertEqual("1", (self.saves / "a.json").read_text())
        self.assertEqual("kept", (self.saves / "b.json").read_text())
        self.assertEqual(["b.json"], os.listdir(old))
        self.assertEqual(["a.json", "b.json"], sorted(os.listdir(self.saves)))

    def test_an_interrupted_copy_leaves_no_save_under_its_name(self):
        """Ctrl-C during the copy: the save directory keeps no truncated
        file, the former save stays, and the next call moves it."""
        old = self.legacy({"rec_1.wav": "x" * 4096})
        with self.cross_filesystem_link(), mock.patch.object(
            self.cli.shutil, "copyfileobj", side_effect=KeyboardInterrupt
        ):
            with self.assertRaises(KeyboardInterrupt):
                self.cli.save_dir()
        self.assertEqual([], os.listdir(self.saves))
        self.assertEqual(["rec_1.wav"], os.listdir(old))
        with self.cross_filesystem_link():
            self.cli.save_dir()
        self.assertEqual("x" * 4096, (self.saves / "rec_1.wav").read_text())

    def test_a_recorded_path_is_found_again_after_the_move(self):
        old = self.legacy({"sample_ch1.wav": "w"})
        recorded = str(old / "sample_ch1.wav")
        self.assertEqual(recorded, self.cli.saved_path(recorded))
        self.cli.save_dir()
        self.assertEqual(
            str(self.saves / "sample_ch1.wav"), self.cli.saved_path(recorded)
        )
        gone = str(old / "never.wav")
        self.assertEqual(gone, self.cli.saved_path(gone))
        self.assertEqual("", self.cli.saved_path(""))


class TestGallerySaves(Copy):
    def gallery(self):
        return load("gallery_copy", self.games / "gallery_server.py")

    def test_the_scan_reads_the_save_path_and_creates_nothing(self):
        gallery = self.gallery()
        self.legacy({"djscratch_state.json": "{}"})
        with mock.patch.object(gallery.subprocess, "run") as run:
            run.return_value = subprocess.CompletedProcess([], 0, "{}", "")
            gallery._scan_games()
        self.assertFalse(self.data.exists())
        self.assertTrue((self.games / "save/djscratch_state.json").exists())


if __name__ == "__main__":
    unittest.main()
