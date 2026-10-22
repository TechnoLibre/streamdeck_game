# © 2026 TechnoLibre (http://www.technolibre.ca)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl)
"""Command line shared by the Stream Deck games.

A game builds its parser here and parses sys.argv before its PIL and
Stream Deck imports: -h and --help print the usage and exit 0, an unknown
argument prints it on stderr and exits 2, and neither imports the Stream
Deck library nor opens the deck. --meta is only accepted here; the game
answers it itself once GAME_META is defined, with that JSON on stdout,
which is what the gallery reads. Only the standard library is imported.

save_dir() is where a game keeps its saves, and saved_path() finds a file
a game recorded by its path after the saves moved there. install_hint() is
the pip line a game prints when PIL or the Stream Deck library is missing.

The name does not match game_*.py: the gallery and the TODO menu list
every game_*.py file as a game."""

import argparse
import os
import shutil

# The version of CONTRACT.md, MAJOR.MINOR: what ERPLibre and the games
# expect of each other. ERPLibre's tests compare its MAJOR with the one
# ERPLibre was built against.
CONTRACT_VERSION = "1.1"

# What the games import beyond the standard library, next to them.
REQUIREMENTS = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "requirements.txt"
)

# Where the saves were kept before save_dir(): save/ next to the games.
LEGACY_SAVE_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "save"
)

EPILOG = """\
Without an option, the game opens the Stream Deck and plays until the
player quits. The gallery (gallery_server.py) runs it in a terminal.
Inside ERPLibre, the gallery and the TODO menu first stop the ERPLibre
Home deck service, which takes the deck back when the game ends."""


def parser(doc):
    """The parser of a game described by `doc`, its module docstring: -h,
    --help and --meta. A game with options of its own adds them to it."""
    p = argparse.ArgumentParser(
        description=doc,
        epilog=EPILOG,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        allow_abbrev=False,
    )
    p.add_argument(
        "--meta",
        action="store_true",
        help="print the game's gallery metadata as JSON and exit",
    )
    return p


def install_hint():
    """The command that installs what the games import."""
    return "pip install -r " + REQUIREMENTS


def save_path():
    """The directory of the saves, without creating or filling it:
    $XDG_DATA_HOME/erplibre-home/streamdeck/save, ~/.local/share standing
    for an unset or relative XDG_DATA_HOME. It lies outside the games'
    repository, so neither repo sync, git clean nor a new clone of the
    games removes it, and a bundle of the checkout does not ship it."""
    base = os.environ.get("XDG_DATA_HOME", "")
    if not os.path.isabs(base):
        base = os.path.join(os.path.expanduser("~"), ".local", "share")
    return os.path.join(base, "erplibre-home", "streamdeck", "save")


def save_dir():
    """save_path(), created if missing, after moving into it the files left
    in LEGACY_SAVE_DIR, one by one, never over a file already there: such a
    file stays where it was. A file another process moves first is skipped.
    Dotfiles stay."""
    path = save_path()
    os.makedirs(path, exist_ok=True)
    try:
        legacy = os.listdir(LEGACY_SAVE_DIR)
    except OSError:
        legacy = []
    for name in legacy:
        source = os.path.join(LEGACY_SAVE_DIR, name)
        if name.startswith(".") or not os.path.isfile(source):
            continue
        _move_no_clobber(source, os.path.join(path, name))
    return path


def _move_no_clobber(source, target):
    """Move the file `source` to `target` unless `target` exists, even when
    another process creates it meanwhile: a hard link, or an exclusive
    create across filesystems, fails rather than replace it. Any failure
    leaves `source` in place."""
    try:
        os.link(source, target)
    except FileExistsError:
        return
    except OSError:
        # Across filesystems: copy to a hidden name, then publish it under
        # `target` by a hard link, which still refuses an existing file. An
        # interrupted copy leaves only the hidden file, which save_dir()
        # and the gallery skip, never a truncated save under its name.
        partial = os.path.join(
            os.path.dirname(target),
            ".%s.partial-%d" % (os.path.basename(target), os.getpid()),
        )
        try:
            with open(source, "rb") as src, open(partial, "xb") as dst:
                shutil.copyfileobj(src, dst)
                dst.flush()
                os.fsync(dst.fileno())
            shutil.copystat(source, partial)
            os.link(partial, target)
        except OSError:
            return
        finally:
            try:
                os.remove(partial)
            except OSError:
                pass
    try:
        os.remove(source)
    except OSError:
        pass


def saved_path(path):
    """`path` when it exists, else the file of that name in save_path() when
    that one does, else `path`. A game that recorded the absolute path of
    one of its saves finds it again after save_dir() moved it."""
    if not path or os.path.exists(path):
        return path
    moved = os.path.join(save_path(), os.path.basename(path))
    return moved if os.path.exists(moved) else path
