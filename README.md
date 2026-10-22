
# streamdeck_game

45 mini games played on the keys of an Elgato Stream Deck, and a web
gallery to browse and launch them. They need Python 3, a Stream Deck and
two Python packages, nothing else.

## Install

The Stream Deck library talks to the deck through hidapi, and the deck
needs a udev rule to open without root. On Debian and Ubuntu:

```
sudo apt install libhidapi-libusb0 python3-venv
sudo tee /etc/udev/rules.d/70-streamdeck.rules <<'EOF'
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", TAG+="uaccess"
KERNEL=="hidraw*", ATTRS{idVendor}=="0fd9", TAG+="uaccess"
EOF
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Fedora uses `hidapi`, Arch Linux `hidapi` as well. Then clone the
repository and install the two packages in a venv:

```
git clone https://github.com/TechnoLibre/streamdeck_game.git
cd streamdeck_game
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Play

Plug the deck in and run a game with the venv's python:

```
.venv/bin/python game_snake.py
.venv/bin/python game_snake.py --help
.venv/bin/python gallery_server.py      # then http://localhost:8042
```

Every game answers `--help`, and `--meta` prints the JSON the gallery
reads. Without an option, it opens the first Stream Deck and plays; games
marked multiplayer use a second deck when one is plugged in. The gallery
opens each game in `gnome-terminal`, or `xterm` without it.

## Saves

Games that keep state write it in
`$XDG_DATA_HOME/erplibre-home/streamdeck/save/` (`~/.local/share` when
`XDG_DATA_HOME` is unset), outside the clone: updating or deleting the clone
leaves them. Saves found in a `save/` directory next to the games, where
older versions kept them, move there on the next run.

## Test

The tests use the standard library only, with fake hardware packages: no
deck and no venv are needed.

```
python3 -m unittest discover -s tests
```

## Inside ERPLibre

[ERPLibre](https://github.com/ERPLibre/ERPLibre) Home clones this repository
at `script/stream_deck/games/` and follows its `main` branch: a commit
pushed here reaches ERPLibre checkouts at their next update. ERPLibre
launches the games from its TODO menu, its make targets and its GNOME
extension; the menu and the gallery first take the deck over from its own
deck service. Its `doc/streamdeck_game.md` describes that side;
`CONTRACT.md` here states what both sides expect of each other.

## License

AGPL-3.0 or later, see `LICENSE`.
