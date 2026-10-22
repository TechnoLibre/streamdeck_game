# Contract between the games and ERPLibre

**Contract version: 1.1**

This repository is cloned by ERPLibre at `script/stream_deck/games/`, by
Google Repo or by `install_erplibre_home.sh --stream-deck`. This file states
what each side relies on. `games_cli.CONTRACT_VERSION` carries the same
version, and ERPLibre records the one it was built against in
`script/stream_deck/games_contract`; the tests of both sides check it.

## What ERPLibre relies on

1. **Layout.** A game is a file `game_<id>.py` at the repository root,
   executable, starting with `#!/usr/bin/env python3`, run as
   `python game_<id>.py`. `<id>` is `[a-z0-9]+`. Every root file matching
   `game_*.py` is a game: the TODO menu, the make targets and the gallery
   list them by that glob. `games_cli.py` and `gallery_server.py` sit next
   to them.
2. **Description.** The first line of a game's module docstring describes
   it in one sentence; the TODO menu shows it when its own translations
   have no `game_<id>` entry.
3. **Command line,** through `games_cli.parser(__doc__)`:
   - `-h` and `--help` print the usage on stdout and exit 0; an unknown
     argument prints it on stderr and exits 2. Both happen before the PIL
     and Stream Deck imports.
   - `--meta` prints one JSON object on stdout and exits 0 within 5 s,
     after those imports but without opening a deck. Required keys:
     `name`, `category`, `multiplayer`, `sdplus`, `description`, `icon`.
     Optional: `saves` (the game keeps saves), `section` (`erplibre`
     files the entry under the extension's ERPLibre tools). Readers ignore
     unknown keys.
4. **Playing.** Without an option the game opens the first Stream Deck,
   plays, and exits when the player quits. It never takes the deck lock:
   the hand-over holds it around the game and passes its exit code on.
5. **Gallery.** `gallery_server.py` serves on port 8042 and launches every
   game through ERPLibre's hand-over. The extension relies on:
   - `GET /api/games`: a JSON array of the `--meta` objects, each with
     `id` added, and `saves` when the save directory holds files of that
     game;
   - `GET /launch/<id>`: 2xx when started; otherwise
     `{"error": "<one line>"}`, with 403 when the `GAMES` setting refuses
     the games and 404 for an unknown id.

   Its other routes (`/stop`, `/api/restart`, `/api/saves…`) serve its own
   page only.
6. **Saves.** A game that keeps state writes it in
   `games_cli.save_dir()`: `$XDG_DATA_HOME/erplibre-home/streamdeck/save/`,
   `~/.local/share` standing for an unset XDG_DATA_HOME. It lies outside
   both repositories: a clone, `repo sync` or `git clean` never touches it.
   Files left in the former `save/` next to the games move there on the
   next run of a game that keeps state or of the gallery, never over a file
   already there. ERPLibre never reads the saves.

## What the games rely on

1. The ERPLibre checkout root is three directories above this repository.
2. `script/install/erplibre_home_handover.sh <command> [arguments…]` runs
   the command under the deck lock, held as program `game`, and exits with
   its code; it exits 4 without running it when `GAMES` is not on, and 2
   when the deck is already held.
3. `script/install/erplibre_home_settings.sh` defines `deck_games_enabled`
   and `deck_games_message`, read by the gallery.
4. The interpreter is `.venv.streamdeck/bin/python`, built from
   `script/stream_deck/requirements.txt`; a game run without it prints the
   `pip install` line for that file.

## Versioning

A change that a reader on the other side can see bumps MAJOR: a new
required `--meta` key, a moved or renamed file, a new exit code, a route
that changes its answer. An optional addition bumps MINOR. ERPLibre's tests
fail when the MAJOR it records differs from this one.

- **1.1:** the saves move out of the repository to `games_cli.save_dir()`.
- **1.0:** the first version.
