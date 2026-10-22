
# streamdeck_game

45 mini-jeux joués sur les touches d'un Elgato Stream Deck, et une galerie
web pour les parcourir et les lancer. Il leur faut Python 3, un Stream Deck
et deux paquets Python, rien d'autre.

## Installer

La bibliothèque Stream Deck parle au deck par hidapi, et le deck demande
une règle udev pour s'ouvrir sans root. Sur Debian et Ubuntu :

```
sudo apt install libhidapi-libusb0 python3-venv
sudo tee /etc/udev/rules.d/70-streamdeck.rules <<'EOF'
SUBSYSTEM=="usb", ATTRS{idVendor}=="0fd9", TAG+="uaccess"
KERNEL=="hidraw*", ATTRS{idVendor}=="0fd9", TAG+="uaccess"
EOF
sudo udevadm control --reload-rules && sudo udevadm trigger
```

Fedora prend `hidapi`, Arch Linux aussi. Puis cloner le dépôt et
installer les deux paquets dans un venv :

```
git clone https://github.com/TechnoLibre/streamdeck_game.git
cd streamdeck_game
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

## Jouer

Branche le deck et lance un jeu avec le python du venv :

```
.venv/bin/python game_snake.py
.venv/bin/python game_snake.py --help
.venv/bin/python gallery_server.py      # puis http://localhost:8042
```

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

```
python3 -m unittest discover -s tests
```

## Dans ERPLibre

[ERPLibre](https://github.com/ERPLibre/ERPLibre) Home clone ce dépôt dans
`script/stream_deck/games/`, épinglé sur une étiquette, et lance les jeux
depuis son menu TODO, ses cibles make et son extension GNOME, en reprenant
le deck à son propre service. Son `doc/streamdeck_game.md` décrit ce côté ;
`CONTRACT.md` dit ici ce que chaque côté attend de l'autre.

## Licence

AGPL-3.0 ou ultérieure, voir `LICENSE`.
