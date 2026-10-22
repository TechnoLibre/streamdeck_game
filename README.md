
# streamdeck_game

45 mini games played on the keys of an Elgato Stream Deck, and a web
gallery to browse and launch them. They are part of ERPLibre Home: ERPLibre
clones this repository at `script/stream_deck/games/` and runs the games
under its Stream Deck venv, after handing the deck over from its deck
service. `CONTRACT.md` states what the games and ERPLibre expect of each
other.

## Install

From an ERPLibre checkout, the Stream Deck level installs the venv and
clones this repository when it is missing:

```
make erplibre_home_streamdeck_install
```

## Play

```
make streamdeck_snake
make streamdeck_gallery      # then http://localhost:8042
./script/todo/todo.py        # Stream Deck › Games
```

Every game answers `--help`, and `--meta` prints the JSON the gallery
reads. Without an option, it opens the first Stream Deck and plays.

## Test

The tests use the standard library only, with fake hardware packages: no
deck and no venv are needed.

```
python3 -m unittest discover -s tests
```

## License

AGPL-3.0 or later, see `LICENSE`.
