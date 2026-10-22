<!---------------------------->
<!-- multilingual suffix: en, fr -->
<!-- no suffix: en -->
<!---------------------------->

<!-- [en] -->
# streamdeck_game

45 mini games played on the keys of an Elgato Stream Deck, and a web
gallery to browse and launch them. They need Python 3, a Stream Deck and
two Python packages, nothing else.

## Install

The Stream Deck library talks to the deck through hidapi, and the deck
needs a udev rule to open without root. On Debian and Ubuntu:

<!-- [fr] -->
# streamdeck_game

45 mini-jeux joués sur les touches d'un Elgato Stream Deck, et une galerie
web pour les parcourir et les lancer. Il leur faut Python 3, un Stream Deck
et deux paquets Python, rien d'autre.

## Installer

La bibliothèque Stream Deck parle au deck par hidapi, et le deck demande
une règle udev pour s'ouvrir sans root. Sur Debian et Ubuntu :

<!-- [end] -->
<!-- [common] -->
```
sudo apt install libhidapi-libusb0 python3-venv
sudo tee /etc/udev/rules.d/70-streamdeck.rules <<'EOF'
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", TAG+="uaccess"
KERNEL=="hidraw*", ATTRS{idVendor}=="0fd9", TAG+="uaccess"
EOF
sudo udevadm control --reload-rules && sudo udevadm trigger
```

<!-- [end] -->
<!-- [en] -->
Fedora uses `hidapi`, Arch Linux `hidapi` as well. Then clone the
repository and install the two packages in a venv:

<!-- [fr] -->
Fedora prend `hidapi`, Arch Linux aussi. Puis cloner le dépôt et
installer les deux paquets dans un venv :

<!-- [end] -->
<!-- [common] -->
```
git clone https://github.com/TechnoLibre/streamdeck_game.git
cd streamdeck_game
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

<!-- [end] -->
<!-- [en] -->
## Play

Plug the deck in and run a game with the venv's python:

```
.venv/bin/python game_snake.py
.venv/bin/python game_snake.py --help
.venv/bin/python gallery_server.py      # then http://localhost:8042
```

<!-- [fr] -->
## Jouer

Branche le deck et lance un jeu avec le python du venv :

```
.venv/bin/python game_snake.py
.venv/bin/python game_snake.py --help
.venv/bin/python gallery_server.py      # puis http://localhost:8042
```

<!-- [end] -->
<!-- [en] -->
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

<!-- [fr] -->
Chaque jeu répond à `--help`, et `--meta` affiche le JSON que lit la
galerie. Sans option, il ouvre le premier Stream Deck et joue ; les jeux
multijoueurs prennent un second deck quand il est branché. La galerie
ouvre chaque jeu dans `gnome-terminal`, ou dans `xterm` à défaut.

## Sauvegardes

Les jeux qui gardent un état l'écrivent dans
`$XDG_DATA_HOME/erplibre-home/streamdeck/save/` (`~/.local/share` quand
`XDG_DATA_HOME` n'est pas défini), hors du clone : mettre à jour ou
supprimer le clone les laisse en place. Les sauvegardes trouvées dans un
répertoire `save/` à côté des jeux, où les versions précédentes les
gardaient, y passent à la prochaine exécution.

## Tester

Les tests n'utilisent que la bibliothèque standard, avec de faux paquets du
matériel : ni deck ni venv n'est nécessaire.

<!-- [end] -->
<!-- [common] -->
```
python3 -m unittest discover -s tests
```

<!-- [end] -->
<!-- [en] -->
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

<!-- [fr] -->
## Dans ERPLibre

[ERPLibre](https://github.com/ERPLibre/ERPLibre) Home clone ce dépôt dans
`script/stream_deck/games/` et suit sa branche `main` : un commit poussé ici
atteint les checkouts d'ERPLibre à leur prochaine mise à jour. ERPLibre
lance les jeux depuis son menu TODO, ses cibles make et son extension
GNOME ; le menu et la galerie reprennent d'abord le deck à son propre
service. Son `doc/streamdeck_game.md` décrit ce côté ; `CONTRACT.md` dit ici
ce que chaque côté attend de l'autre.

## Licence

AGPL-3.0 ou ultérieure, voir `LICENSE`.

<!-- [end] -->
