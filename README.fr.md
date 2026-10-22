
# streamdeck_game

45 mini-jeux joués sur les touches d'un Elgato Stream Deck, et une galerie
web pour les parcourir et les lancer. Ils font partie d'ERPLibre Home :
ERPLibre clone ce dépôt dans `script/stream_deck/games/` et lance les jeux
sous son venv Stream Deck, après avoir repris le deck à son service.
`CONTRACT.md` dit ce que les jeux et ERPLibre attendent l'un de l'autre.

## Installer

Depuis un checkout d'ERPLibre, le niveau Stream Deck installe le venv et
clone ce dépôt quand il manque :

```
make erplibre_home_streamdeck_install
```

## Jouer

```
make streamdeck_snake
make streamdeck_gallery      # then http://localhost:8042
./script/todo/todo.py        # Stream Deck › Games
```

Chaque jeu répond à `--help`, et `--meta` affiche le JSON que lit la
galerie. Sans option, il ouvre le premier Stream Deck et joue.

## Tester

Les tests n'utilisent que la bibliothèque standard, avec de faux paquets du
matériel : ni deck ni venv n'est nécessaire.

```
python3 -m unittest discover -s tests
```

## Licence

AGPL-3.0 ou ultérieure, voir `LICENSE`.
