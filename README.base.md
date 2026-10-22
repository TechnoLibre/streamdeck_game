<!---------------------------->
<!-- multilingual suffix: en, fr -->
<!-- no suffix: en -->
<!---------------------------->

<!-- [en] -->
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

<!-- [fr] -->
# streamdeck_game

45 mini-jeux joués sur les touches d'un Elgato Stream Deck, et une galerie
web pour les parcourir et les lancer. Ils font partie d'ERPLibre Home :
ERPLibre clone ce dépôt dans `script/stream_deck/games/` et lance les jeux
sous son venv Stream Deck, après avoir repris le deck à son service.
`CONTRACT.md` dit ce que les jeux et ERPLibre attendent l'un de l'autre.

## Installer

Depuis un checkout d'ERPLibre, le niveau Stream Deck installe le venv et
clone ce dépôt quand il manque :

<!-- [end] -->
<!-- [common] -->
```
make erplibre_home_streamdeck_install
```

<!-- [end] -->
<!-- [en] -->
## Play

<!-- [fr] -->
## Jouer

<!-- [end] -->
<!-- [common] -->
```
make streamdeck_snake
make streamdeck_gallery      # then http://localhost:8042
./script/todo/todo.py        # Stream Deck › Games
```

<!-- [end] -->
<!-- [en] -->
Every game answers `--help`, and `--meta` prints the JSON the gallery
reads. Without an option, it opens the first Stream Deck and plays.

## Test

The tests use the standard library only, with fake hardware packages: no
deck and no venv are needed.

<!-- [fr] -->
Chaque jeu répond à `--help`, et `--meta` affiche le JSON que lit la
galerie. Sans option, il ouvre le premier Stream Deck et joue.

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
## License

AGPL-3.0 or later, see `LICENSE`.

<!-- [fr] -->
## Licence

AGPL-3.0 ou ultérieure, voir `LICENSE`.

<!-- [end] -->
