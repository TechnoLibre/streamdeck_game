#!/usr/bin/env python3
# © 2026 TechnoLibre (http://www.technolibre.ca)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
"""The repository on its own, standard library only.

The gallery and games_cli are copied into a temporary directory (Copy, from
test_saves), so the presence of ERPLibre three levels up is the test's own.

    python3 -m unittest discover -s tests
"""

import os
import shlex
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from test_saves import Copy, load

ROOT = Path(__file__).resolve().parent.parent


class TestInstallHint(Copy):
    def test_the_install_hint_names_the_requirements_next_to_it(self):
        self.assertEqual(
            "pip install -r %s" % (self.games / "requirements.txt"),
            self.cli.install_hint(),
        )


class TestGameInstallHint(unittest.TestCase):
    def test_a_game_without_pil_names_the_repository_requirements(self):
        with tempfile.TemporaryDirectory() as tmp:
            fake = Path(tmp, "PIL")
            fake.mkdir()
            (fake / "__init__.py").write_text("raise ImportError('no PIL')\n")
            res = subprocess.run(
                [sys.executable, str(ROOT / "game_snake.py")],
                env=dict(os.environ, PYTHONPATH=tmp),
                capture_output=True,
                text=True,
                timeout=30,
            )
        self.assertNotEqual(0, res.returncode)
        self.assertEqual(
            "pip install -r %s" % (ROOT / "requirements.txt"),
            res.stdout.strip(),
        )


class TestGalleryAlone(Copy):
    """Without ERPLibre three levels up, no GAMES setting refuses the games
    and a game runs without the hand-over; with it, both are used."""

    def gallery(self):
        return load("gallery_copy", self.games / "gallery_server.py")

    def test_without_erplibre(self):
        gallery = self.gallery()
        self.assertIsNone(gallery._games_refusal())
        words = shlex.split(gallery._game_bash_cmd("/x/game_demo.py"))
        self.assertEqual(["cd", str(self.games), "&&", "bash", "-c"], words[:5])
        self.assertNotIn("handover", " ".join(words))

    def test_the_loop_really_runs_without_erplibre(self):
        game = self.tmp / "game_demo.py"
        game.write_text("print('played')\n")
        gallery = self.gallery()
        res = subprocess.run(
            ["bash", "-c", gallery._game_bash_cmd(str(game))],
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual("played", res.stdout.splitlines()[0])

    def test_inside_erplibre(self):
        # games/ at <tmp>/a/b/c/games: ERPLibre's root is <tmp>/a.
        install = self.tmp / "a/script/install"
        install.mkdir(parents=True)
        (install / "erplibre_home_handover.sh").write_text("")
        (install / "erplibre_home_settings.sh").write_text(
            "deck_games_enabled() { false; }\n"
            "deck_games_message() { echo 'games are off'; }\n"
        )
        gallery = self.gallery()
        self.assertEqual("games are off", gallery._games_refusal())
        words = shlex.split(gallery._game_bash_cmd("/x/game_demo.py"))
        self.assertEqual(
            ["cd", str(self.tmp / "a"), "&&",
             str(install / "erplibre_home_handover.sh"), "bash", "-c"],
            words[:6],
        )


if __name__ == "__main__":
    unittest.main()
