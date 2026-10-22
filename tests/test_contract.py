#!/usr/bin/env python3
# © 2026 TechnoLibre (http://www.technolibre.ca)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
"""The games' half of CONTRACT.md, checked with the standard library only.

Every game runs under the test's python with fake hardware packages first
on PYTHONPATH: importing the killing fakes writes a witness file and exits
99, so a game that goes past its command line never reaches a real deck.
The importable fakes let a game define GAME_META and answer --meta; only
DeviceManager().enumerate(), the first step towards a deck, kills it, with
77. XDG_RUNTIME_DIR points at an empty directory: a game that took the deck
lock would leave its file there.

    python3 -m unittest discover -s tests
"""

import concurrent.futures
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parent.parent
GAME_FILE = re.compile(r"^game_[a-z0-9]+\.py$")
REQUIRED_META = {
    "name",
    "category",
    "multiplayer",
    "sdplus",
    "description",
    "icon",
}
IMPORT = re.compile(r"^\s*(?:import|from)\s+(\w+)", re.M)

KILLING_FAKE = """import os
with open(os.environ["HARDWARE_WITNESS"], "w") as f:
    f.write(__name__)
os._exit(99)
"""
HARDWARE_PACKAGES = ("StreamDeck", "PIL", "cv2", "requests", "pyudev")
FAKE_WEBBROWSER = """import builtins
import os


def open(*_args, **_kw):
    with builtins.open(os.environ["HARDWARE_WITNESS"], "w") as f:
        f.write("webbrowser")
    os._exit(98)
"""
ANYTHING = """class _Anything:
    def __getattr__(self, _name):
        return _Anything()

    def __call__(self, *_args, **_kw):
        return _Anything()


def __getattr__(_name):
    return _Anything()
"""
FAKE_DEVICE_MANAGER = """import os


class DeviceManager:
    def enumerate(self):
        with open(os.environ["HARDWARE_WITNESS"], "w") as f:
            f.write("enumerate")
        os._exit(77)
"""
IMPORTABLE_HARDWARE = {
    "PIL/__init__.py": ANYTHING,
    "StreamDeck/__init__.py": "",
    "StreamDeck/DeviceManager.py": FAKE_DEVICE_MANAGER,
    "StreamDeck/Devices/__init__.py": "",
    "StreamDeck/Devices/StreamDeck.py": ANYTHING,
    "StreamDeck/ImageHelpers.py": ANYTHING,
    "StreamDeck/Transport/__init__.py": "",
    "StreamDeck/Transport/Transport.py": (
        "class TransportError(Exception):\n    pass\n"
    ),
}


def games():
    """The game files of the repository root, sorted."""
    return sorted(ROOT.glob("game_*.py"))


def run_without_hardware(script, *args, fakes=None):
    """Runs `script` with the fake packages, a fake webbrowser and an empty
    XDG_RUNTIME_DIR. Returns the CompletedProcess, whether a fake wrote its
    witness, and the content of XDG_RUNTIME_DIR. Asserts nothing, so a
    thread can call it. `fakes`, {relative path: source}, replaces the
    killing fakes, for instance with IMPORTABLE_HARDWARE."""
    if fakes is None:
        fakes = {
            "%s/__init__.py" % package: KILLING_FAKE
            for package in HARDWARE_PACKAGES
        }
    with tempfile.TemporaryDirectory() as tmp:
        fake_dir = os.path.join(tmp, "fakes")
        sources = dict(fakes, **{"webbrowser/__init__.py": FAKE_WEBBROWSER})
        for relative, source in sources.items():
            path = os.path.join(fake_dir, relative)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(source)
        run_dir = os.path.join(tmp, "run")
        os.makedirs(run_dir, mode=0o700)
        witness = os.path.join(tmp, "witness")
        env = dict(
            os.environ,
            PYTHONPATH=fake_dir,
            XDG_RUNTIME_DIR=run_dir,
            XDG_CONFIG_HOME=os.path.join(tmp, "config"),
            XDG_CACHE_HOME=os.path.join(tmp, "cache"),
            XDG_DATA_HOME=os.path.join(tmp, "data"),
            HOME=os.path.join(tmp, "home"),
            HARDWARE_WITNESS=witness,
        )
        res = subprocess.run(
            [sys.executable, str(script)] + list(args),
            cwd=tmp,
            env=env,
            capture_output=True,
            text=True,
            timeout=30,
        )
        return res, os.path.exists(witness), os.listdir(run_dir)


def run_all(*args, fakes=None):
    """(file name, CompletedProcess, witness written, run dir) for every
    game, eight at a time."""
    paths = games()
    with concurrent.futures.ThreadPoolExecutor(8) as pool:
        results = list(
            pool.map(
                lambda p: run_without_hardware(p, *args, fakes=fakes), paths
            )
        )
    return [(p.name,) + r for p, r in zip(paths, results)]


class TestLayout(unittest.TestCase):
    def test_every_game_is_named_executable_and_has_its_shebang(self):
        self.assertEqual(45, len(games()))
        for game in games():
            with self.subTest(game=game.name):
                self.assertRegex(game.name, GAME_FILE)
                self.assertTrue(os.access(game, os.X_OK))
                first = game.read_text(encoding="utf-8").split("\n")[0]
                self.assertEqual("#!/usr/bin/env python3", first)

    def test_every_game_opens_on_a_one_line_description(self):
        """The TODO menu shows the docstring's first line."""
        for game in games():
            with self.subTest(game=game.name):
                doc = game.read_text(encoding="utf-8").split('"""')[1]
                self.assertTrue(doc.split("\n")[0].strip())

    def test_every_game_reads_its_command_line_through_games_cli(self):
        for game in games():
            with self.subTest(game=game.name):
                text = game.read_text(encoding="utf-8")
                self.assertIn("\nimport games_cli\n", text)
                self.assertIn("games_cli.parser(__doc__)", text)

    def test_no_game_imports_a_sibling_but_games_cli(self):
        siblings = {p.stem for p in ROOT.glob("*.py")} - {"games_cli"}
        for game in games():
            with self.subTest(game=game.name):
                imported = set(IMPORT.findall(game.read_text("utf-8")))
                self.assertEqual(set(), imported & siblings)

    def test_games_cli_is_not_a_game_and_imports_the_stdlib_only(self):
        cli = ROOT / "games_cli.py"
        self.assertNotIn(cli, games())
        imported = set(IMPORT.findall(cli.read_text(encoding="utf-8")))
        self.assertEqual({"argparse", "os", "shutil"}, imported)

    def test_the_gallery_and_its_page_exist(self):
        self.assertTrue((ROOT / "gallery_server.py").is_file())
        self.assertTrue((ROOT / "index.html").is_file())


class TestContractVersion(unittest.TestCase):
    def test_games_cli_carries_the_version_of_contract_md(self):
        spec = importlib.util.spec_from_file_location(
            "games_cli", ROOT / "games_cli.py"
        )
        cli = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(cli)
        self.assertRegex(cli.CONTRACT_VERSION, r"^\d+\.\d+$")
        text = (ROOT / "CONTRACT.md").read_text(encoding="utf-8")
        found = re.findall(r"\*\*Contract version: (\d+\.\d+)\*\*", text)
        self.assertEqual([cli.CONTRACT_VERSION], found)


class TestCommandLine(unittest.TestCase):
    """-h, --help and an unknown option end before the hardware imports and
    without the deck lock; without an option, a game goes on to them."""

    def test_help_prints_the_usage_and_exits_0(self):
        for option in ("-h", "--help"):
            for name, res, imported, run_dir in run_all(option):
                with self.subTest(game=name, option=option):
                    self.assertFalse(imported, res.stderr)
                    self.assertEqual([], run_dir)
                    self.assertEqual(0, res.returncode, res.stderr)
                    self.assertIn("usage: %s" % name, res.stdout)
                    self.assertIn("--meta", res.stdout)
                    self.assertEqual("", res.stderr)

    def test_an_unknown_option_exits_2_with_the_usage(self):
        for name, res, imported, run_dir in run_all("--bogus"):
            with self.subTest(game=name):
                self.assertFalse(imported, res.stderr)
                self.assertEqual([], run_dir)
                self.assertEqual(2, res.returncode, res.stderr)
                self.assertIn("usage:", res.stderr)
                self.assertEqual("", res.stdout)

    def test_without_an_option_every_game_goes_on_to_the_hardware(self):
        for name, res, imported, run_dir in run_all():
            with self.subTest(game=name):
                self.assertTrue(imported, res.stderr)
                self.assertEqual(99, res.returncode, res.stderr)
                self.assertEqual([], run_dir)

    def test_the_options_of_a_game_are_still_read(self):
        """Hangman and Minesweeper add theirs to the shared parser."""
        for game, args in (
            ("game_hangman.py", ["-l", "en"]),
            ("game_minesweeper.py", ["-m", "6", "-v"]),
        ):
            res, imported, _ = run_without_hardware(ROOT / game, *args)
            self.assertTrue(imported, res.stderr)
            self.assertEqual(99, res.returncode, (game, res.stderr))
        res, imported, _ = run_without_hardware(
            ROOT / "game_hangman.py", "-l", "de"
        )
        self.assertFalse(imported, res.stderr)
        self.assertEqual(2, res.returncode, res.stderr)


class TestMeta(unittest.TestCase):
    def test_every_game_answers_meta_with_the_required_keys(self):
        for name, res, imported, run_dir in run_all(
            "--meta", fakes=IMPORTABLE_HARDWARE
        ):
            with self.subTest(game=name):
                self.assertFalse(imported, res.stderr)
                self.assertEqual([], run_dir)
                self.assertEqual(0, res.returncode, res.stderr)
                meta = json.loads(res.stdout)
                self.assertLessEqual(REQUIRED_META, set(meta))
                self.assertIsInstance(meta["multiplayer"], bool)
                self.assertIsInstance(meta["sdplus"], bool)

    def test_meta_answers_wherever_it_stands_among_the_options(self):
        for game, args in (
            ("game_hangman.py", ["-l", "en", "--meta"]),
            ("game_minesweeper.py", ["-v", "--meta", "-m", "3"]),
        ):
            with self.subTest(game=game, args=args):
                res, imported, _ = run_without_hardware(
                    ROOT / game, *args, fakes=IMPORTABLE_HARDWARE
                )
                self.assertFalse(imported, res.stderr)
                self.assertEqual(0, res.returncode, res.stderr)
                self.assertIn("name", json.loads(res.stdout))

    def test_the_importable_fake_reaches_the_deck(self):
        """The witness of the tests above: without --meta, the same fake
        leads a game to enumerate()."""
        res, imported, _ = run_without_hardware(
            ROOT / "game_hangman.py", "-l", "en", fakes=IMPORTABLE_HARDWARE
        )
        self.assertTrue(imported, res.stderr)
        self.assertEqual(77, res.returncode, res.stderr)


class TestGallery(unittest.TestCase):
    """The gallery answers its command line without listening, launching a
    game or opening a browser, and lists exactly the root game files."""

    SCRIPT = ROOT / "gallery_server.py"

    def test_help_prints_the_usage_and_exits_0(self):
        for option in ("-h", "--help"):
            res, imported, run_dir = run_without_hardware(self.SCRIPT, option)
            self.assertFalse(imported, res.stderr)
            self.assertEqual([], run_dir)
            self.assertEqual(0, res.returncode, res.stderr)
            self.assertIn("http://localhost:8042", res.stdout)

    def test_an_unknown_option_exits_2_with_the_usage(self):
        for args in (["--bogus"], ["8042"]):
            res, imported, _ = run_without_hardware(self.SCRIPT, *args)
            self.assertFalse(imported, res.stderr)
            self.assertEqual(2, res.returncode, args)
            self.assertIn("usage:", res.stderr, args)

    def test_api_games_lists_every_game_with_its_id(self):
        """The real glob; only the --meta subprocess is simulated."""
        spec = importlib.util.spec_from_file_location(
            "gallery_server", self.SCRIPT
        )
        gallery = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(gallery)
        scanned = []

        def meta(argv, **_kw):
            scanned.append(argv[1])
            self.assertEqual("--meta", argv[2])
            return subprocess.CompletedProcess(argv, 0, '{"name": "x"}', "")

        with mock.patch.object(gallery.subprocess, "run", side_effect=meta):
            listed = gallery._scan_games()
        self.assertEqual([str(p) for p in games()], sorted(scanned))
        self.assertEqual(
            sorted(p.stem[len("game_") :] for p in games()),
            sorted(g["id"] for g in listed),
        )


if __name__ == "__main__":
    unittest.main()
