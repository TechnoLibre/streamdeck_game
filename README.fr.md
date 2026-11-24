
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

## Jeux

Les 45 jeux, avec leurs contrôles et ce qu'apporte un second deck.
Chaque jeu se lance par `.venv/bin/python game_<id>.py` ; dans ERPLibre,
`make streamdeck_<id>` lance le même fichier par la passation d'ERPLibre.
Dans la colonne 2 joueurs, VS oppose deux decks et Coop leur fait partager
un plateau. Dans la colonne Genre, SD+ marque un mode pour le Stream Deck +,
avec ses dials et son écran tactile.

| Jeu | Fichier | Genre | 2 joueurs |
|-----|---------|-------|-----------|
| Snake | `game_snake.py` | Arcade | VS |
| Breakout | `game_breakout.py` | Arcade / SD+ | - |
| Flappy Bird | `game_flappy.py` | Arcade | - |
| Pong | `game_pong.py` | Arcade / SD+ | VS |
| Bomberman | `game_bomberman.py` | Arcade | VS |
| Pac-Man | `game_pacman.py` | Arcade / SD+ | - |
| Space Invaders | `game_spaceinvaders.py` | Arcade | - |
| Frogger | `game_frogger.py` | Arcade | - |
| Tetris | `game_tetris.py` | Arcade / SD+ | - |
| Tower Defense | `game_towerdefense.py` | Arcade | - |
| Pinball | `game_pinball.py` | Arcade | - |
| Whack-a-Mole | `game_whackamole.py` | Réflexe | VS |
| Reaction Time | `game_reaction.py` | Réflexe | VS |
| Simon Says | `game_simon.py` | Mémoire | VS |
| Color Match | `game_colormatch.py` | Mémoire | VS |
| Minesweeper | `game_minesweeper.py` | Puzzle | VS |
| Lights Out | `game_lightsout.py` | Puzzle | Coop |
| 2048 | `game_2048.py` | Puzzle | - |
| Taquin | `game_taquin.py` | Puzzle | - |
| Sokoban | `game_sokoban.py` | Puzzle | - |
| Flood Fill | `game_floodfill.py` | Puzzle | VS |
| Sudoku 3x3 | `game_sudoku.py` | Puzzle | - |
| Maze Runner | `game_maze.py` | Puzzle | - |
| Battleship | `game_battleship.py` | Stratégie | VS |
| Mastermind | `game_mastermind.py` | Déduction | - |
| Tic-Tac-Toe | `game_tictactoe.py` | Stratégie | VS |
| Connect 4 | `game_connect4.py` | Stratégie | VS |
| Checkers | `game_checkers.py` | Stratégie | VS |
| Reversi | `game_reversi.py` | Stratégie | VS |
| Wordle | `game_wordle.py` | Mot | - |
| Hangman | `game_hangman.py` | Mot / SD+ | - |
| Number Guess | `game_numberguess.py` | Devinette | - |
| Rock Paper Scissors | `game_rps.py` | Rapide | VS |
| Top-Down Racer | `game_racer.py` | Course | - |
| Drag Race | `game_dragrace.py` | Course | VS |
| Racing+ | `game_racingplus.py` | SD+ Course | - |
| Game of Life | `game_life.py` | Simulation | - |
| Langton's Ant | `game_langton.py` | Simulation | - |
| Safe Cracker | `game_safecracker.py` | SD+ Puzzle | - |
| Slot Machine | `game_slots.py` | SD+ Arcade | - |
| Color Mixer | `game_colormixer.py` | SD+ Puzzle | - |
| DJ Scratch | `game_djscratch.py` | SD+ Musique | - |
| Fishing | `game_fishing.py` | SD+ Arcade | - |
| Piano | `game_piano.py` | SD+ Musique | - |
| Thermometer | `game_thermometer.py` | SD+ Devinette | - |


### Arcade

#### Snake

Classique. Le serpent grandit en mangeant la nourriture. Vitesse augmente avec le score. Wrap-around aux bords.

- **Contrôles** : appuie n'importe quel bouton pour tourner le serpent vers cette direction
- **2 joueurs** : deux serpents (vert/bleu) sur la même grille. Collision avec l'autre = mort


#### Breakout

Casse-briques pivoté 90°. Briques à gauche, paddle à droite, balle rebondit horizontalement.

- **Contrôles** : appuie sur la colonne de droite pour placer le paddle, ou n'importe où pour le déplacer
- **Stream Deck +** : le jeu se joue sur l'écran tactile, le dial déplace le paddle ; les briques cassées lâchent parfois un item


#### Flappy Bird

L'oiseau avance de gauche à droite, les obstacles (tuyaux) défilent. Gravité tire l'oiseau vers le bas.

- **Contrôles** : appuie n'importe quel bouton pour monter d'une case


#### Pong

Pong classique pivoté 90°. Paddle gauche vs paddle droite. Premier à 5 points gagne.

- **1 joueur** : colonne gauche = toi, droite = IA
- **2 joueurs** : chaque deck contrôle un paddle, appuie pour placer à cette ligne
- **Stream Deck +** : le jeu se joue sur l'écran tactile 800x100, un dial déplace le paddle, le toucher le place


#### Bomberman

Déplace ton personnage, pose des bombes, détruis les murs. Ne te fais pas exploser!

- **Contrôles** : appuie adjacent pour bouger, appuie sur ta position pour poser une bombe (3s de délai)
- **2 joueurs** : P1 (bleu) et P2 (orange) sur la même grille. Dernier vivant gagne


### Réflexe

#### Whack-a-Mole

Des taupes apparaissent aléatoirement pendant 30 secondes. Tape-les! La vitesse augmente avec le score. 3 secondes de cooldown en fin de partie pour voir le score.

- **2 joueurs** : mêmes taupes sur les deux decks, scores séparés. Le plus haut gagne


#### Reaction Time

Un bouton vert s'allume après un délai aléatoire. Tape-le le plus vite possible! 5 rounds, temps en millisecondes.

- **2 joueurs** : même cible, le plus rapide gagne chaque round. Moyenne comparée à la fin


### Mémoire

#### Simon Says

Le deck joue une séquence lumineuse. Reproduis-la dans l'ordre. La séquence s'allonge à chaque tour.

- **2 joueurs** : même séquence sur les deux decks. Le premier à se tromper perd


#### Color Match

Jeu de mémoire de paires. Retourne deux cartes : si elles sont de la même couleur, elles restent révélées. Trouve toutes les paires.

- **2 joueurs** : même plateau, chacun retourne sur son deck. Le joueur avec le plus de paires gagne


### Puzzle

#### Minesweeper

Démineur classique avec animation de flag (barre jaune progressive en appui long).

- **Contrôles** : appui court = révéler, appui long (0.6s) = poser/retirer drapeau, appui sur chiffre = chord (révéler voisins si drapeaux corrects)
- **2 joueurs (VS Mine Hunter)** : règles inversées! Trouve les mines pour marquer. Mine = +1 + garde ton tour. Case safe = tour de l'adversaire. Flood-fill sur les cases vides. Le joueur avec le plus de mines trouvées gagne
- **Paramètres** : `-m N` pour changer le nombre de mines, `-v` pour afficher les paramètres


```
.venv/bin/python game_minesweeper.py -m 6   # 6 mines
.venv/bin/python game_minesweeper.py -v     # show params / afficher paramètres
```


#### Lights Out

Appuie un bouton pour le toggle ainsi que ses 4 voisins. Éteins toutes les lumières pour gagner.

- **2 joueurs (coop)** : grille partagée! Les deux joueurs agissent sur le même plateau


#### 2048

Fusionne les tuiles de même valeur pour atteindre 2048. Couleurs distinctes par valeur.

- **Contrôles** : coins = directions (haut-gauche=haut, haut-droite=droite, bas-gauche=gauche, bas-droite=bas). Ou appuie la moitié gauche/droite pour aller dans cette direction


#### Taquin (Sliding Puzzle)

Tuiles numérotées à remettre en ordre (1→N) en les glissant vers la case vide. N = nombre de boutons - 1.

- **Contrôles** : appuie une tuile adjacente à la case vide pour la déplacer


#### Sokoban

Pousse les boîtes (B) sur les cibles (X). Toutes les boîtes sur les cibles = victoire.

- **Contrôles** : appuie adjacent pour bouger. Si une boîte est devant, elle est poussée


#### Flood Fill

La grille a des couleurs aléatoires. Choisis une couleur dans la rangée du bas pour flood-fill depuis le coin haut-gauche. Remplis toute la grille en un nombre limité de coups.

- **2 joueurs** : même grille de départ, chacun joue indépendamment. Premier à remplir gagne


### Stratégie / Déduction

#### Battleship

Bataille navale. Les bateaux sont cachés. Tire pour les trouver.

- **1 joueur** : grille solo, trouve tous les bateaux
- **2 joueurs** : chaque deck = grille d'attaque privée. Touché = garde ton tour. Manqué = tour de l'adversaire. Bateaux coulés en rouge foncé. Bateaux révélés en fin de partie


#### Mastermind

Devine le code secret de couleurs. Rangée du bas = ton essai (appuie pour cycler les couleurs). Haut-droite = soumettre. Feedback après chaque essai : E = exact (bonne couleur, bonne place), P = partiel (bonne couleur, mauvaise place).


#### Tic-Tac-Toe

Morpion classique sur une grille 3x3 centrée sur le deck.

- **1 joueur** : hot seat, les joueurs alternent sur le même deck
- **2 joueurs** : chaque deck = un joueur (X ou O). Seul le deck du joueur actif accepte les inputs. L'autre affiche "WAIT"


#### Connect 4

Lâche des pièces dans une colonne ; le premier à en aligner 4 gagne. Le jeu demande au départ une IA ou un second joueur.

- **Contrôles** : appuie sur la rangée du haut pour lâcher une pièce dans cette colonne
- **2 joueurs** : sur le même deck, ou sur deux decks quand les deux sont branchés


#### Wordle

Devine un mot de 5 lettres. Rangée du bas = lettres (appuie pour cycler A-Z). Dernier bouton = soumettre. Vert = bonne lettre bonne place, jaune = bonne lettre mauvaise place, gris = absent. 6 essais.


#### Checkers

Dames simplifiées. Sélectionne une pièce puis appuie la destination. Déplacements diagonaux. Saute pour capturer.

- **2 joueurs** : rouge vs bleu, chacun son deck


#### Reversi / Othello

Place des pièces pour retourner celles de l'adversaire. Le plus de pièces à la fin gagne.

- **1 joueur** : vs IA (stratégie simple)
- **2 joueurs** : noir vs blanc


### Arcade (suite)

#### Pac-Man

Mange tous les points. Évite le fantôme! Appuie pour changer de direction. Le fantôme te chasse.

- **Stream Deck +** : le jeu se joue sur l'écran tactile, les dials dirigent, un appui sur un dial démarre


#### Space Invaders

Les aliens descendent. Tu es sur la rangée du bas. Appuie ta position pour tirer, appuie adjacent pour bouger.


#### Frogger

Traverse la route. Les voitures défilent. Saute de case en case pour atteindre le haut!


#### Tetris

Pièces tombent de droite à gauche (pivoté 90°). Rangée du haut = rotation, bas = drop, milieu = déplacer.

- **Stream Deck +** : le jeu se joue sur l'écran tactile, les dials contrôlent la pièce


#### Tower Defense

Les ennemis traversent la rangée du milieu. Place des tours au-dessus/en-dessous pour les éliminer. Survie 5 vagues!


#### Pinball

Flipper vertical : tourne le deck de 90° pour que son grand côté soit debout. Garde la balle en jeu, touche les bumpers, bats ton score.

- **Contrôles** : la colonne de droite porte les flippers, moitié haute = flipper gauche, moitié basse = flipper droit ; appuie sur un flipper pour lancer la balle


### Mot / Devinette

#### Hangman

Chaque bouton = une lettre. Appuie pour deviner. 6 erreurs = game over. Le mot s'affiche sur la rangée du haut, ou sur l'écran tactile d'un Stream Deck +.


#### Number Guess

Devine un nombre 1-100. Les boutons affichent des valeurs. Couleurs = chaud/froid. Moins d'essais = meilleur score.


#### Rock Paper Scissors

3 boutons : pierre, papier, ciseaux. Best of 5.

- **2 joueurs** : choix simultané, révélation!


### Puzzle (suite)

#### Sudoku 3x3

Grille 3x3 simplifiée centrée sur le deck. Appuie pour cycler les chiffres. Pas de répétitions en lignes/colonnes.


#### Maze Runner

Labyrinthe généré aléatoirement. Navigue du coin haut-gauche au bas-droite. Appuie les cases adjacentes pour bouger.


### Course

#### Top-Down Racer

La route défile de droite à gauche. Esquive les obstacles ; la vitesse augmente avec le temps. Jusqu'où iras-tu?

- **Contrôles** : appuie sur les rangées du haut ou du bas pour changer de voie


#### Drag Race

Passe les vitesses au bon régime : trop tôt, c'est lent, trop tard, c'est la zone rouge. Les boutons s'allument à mesure que le régime monte. Le meilleur temps gagne.

- **Contrôles** : appuie quand la zone verte s'allume pour passer la vitesse
- **2 joueurs** : course côte à côte, un deck chacun


### Simulation

#### Game of Life

Automate cellulaire de Conway. Les cellules vivent ou meurent selon leurs voisins. Wrap-around aux bords.

- **Contrôles** : appuie pour toggle une cellule. Haut-gauche = play/pause. Haut-droite = randomize. Bas-droite = clear


#### Langton's Ant

Automate cellulaire : une fourmi se déplace sur la grille. Sur blanc → tourne à droite + noir. Sur noir → tourne à gauche + blanc. Motifs émergents!


### Stream Deck + (dials + touchscreen)

#### Safe Cracker

Tourne les 4 dials pour deviner une combinaison 4 chiffres. Barres chaud/froid sur le touchscreen. Click = lock.


#### Slot Machine

Click un dial pour spinner toutes les roues. Click chaque dial pour stopper sa roue. 3 identiques = jackpot!


#### Color Mixer

3 dials = Rouge, Vert, Bleu. Mixe pour matcher la couleur cible affichée sur le touchscreen. Dial 4 = soumettre.


#### DJ Scratch

Tourne les dials pour scratcher du vinyl. Waveforms animées sur le touchscreen. Click = changer de style (sine/square/saw/noise).


#### Fishing

Click dial = lancer. Quand le poisson mord (touchscreen flash), tourne pour mouliner! Trop vite = la ligne casse.


#### Piano

Rangée du bas = touches de piano (C D E F G A B). Dial 1 = changer d'octave. Couleurs par note sur le touchscreen.


#### Thermometer

Tourne le dial pour deviner la température secrète. Barre thermomètre sur le touchscreen avec gradient chaud/froid.


#### Racing+

Course à défilement latéral sur l'écran tactile. Les obstacles défilent de droite à gauche ; évite-les, ainsi que les murs, pendant que la vitesse monte.

- **Contrôles** : un dial dirige vers le haut et le bas

## Dans ERPLibre

[ERPLibre](https://github.com/ERPLibre/ERPLibre) Home clone ce dépôt dans
`script/stream_deck/games/` et suit sa branche `main` : un commit poussé ici
atteint les checkouts d'ERPLibre à leur prochaine mise à jour. ERPLibre
lance les jeux depuis son menu TODO, `make streamdeck_<id>` et la galerie
de son extension GNOME ; les trois passent par sa passation, qui reprend le
deck à son propre service le temps de la partie. Son
`doc/streamdeck_game.md` décrit ce côté ; `CONTRACT.md` dit ici ce que
chaque côté attend de l'autre.

## Licence

AGPL-3.0 ou ultérieure, voir `LICENSE`.
