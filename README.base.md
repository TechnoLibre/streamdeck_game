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
## Games

The 45 games, with their controls and what a second deck adds.
Every game runs with `.venv/bin/python game_<id>.py`; inside ERPLibre,
`make streamdeck_<id>` runs the same file through ERPLibre's hand-over.
In the 2 players column, VS pits two decks against each other and Coop
shares one board between them. In the Kind column, SD+ marks a mode for
the Stream Deck +, with its dials and touchscreen.

| Game | File | Kind | 2 players |
|------|------|------|-----------|
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
| Whack-a-Mole | `game_whackamole.py` | Reflex | VS |
| Reaction Time | `game_reaction.py` | Reflex | VS |
| Simon Says | `game_simon.py` | Memory | VS |
| Color Match | `game_colormatch.py` | Memory | VS |
| Minesweeper | `game_minesweeper.py` | Puzzle | VS |
| Lights Out | `game_lightsout.py` | Puzzle | Coop |
| 2048 | `game_2048.py` | Puzzle | - |
| Taquin | `game_taquin.py` | Puzzle | - |
| Sokoban | `game_sokoban.py` | Puzzle | - |
| Flood Fill | `game_floodfill.py` | Puzzle | VS |
| Sudoku 3x3 | `game_sudoku.py` | Puzzle | - |
| Maze Runner | `game_maze.py` | Puzzle | - |
| Battleship | `game_battleship.py` | Strategy | VS |
| Mastermind | `game_mastermind.py` | Deduction | - |
| Tic-Tac-Toe | `game_tictactoe.py` | Strategy | VS |
| Connect 4 | `game_connect4.py` | Strategy | VS |
| Checkers | `game_checkers.py` | Strategy | VS |
| Reversi | `game_reversi.py` | Strategy | VS |
| Wordle | `game_wordle.py` | Word | - |
| Hangman | `game_hangman.py` | Word / SD+ | - |
| Number Guess | `game_numberguess.py` | Guess | - |
| Rock Paper Scissors | `game_rps.py` | Quick | VS |
| Top-Down Racer | `game_racer.py` | Race | - |
| Drag Race | `game_dragrace.py` | Race | VS |
| Racing+ | `game_racingplus.py` | SD+ Race | - |
| Game of Life | `game_life.py` | Simulation | - |
| Langton's Ant | `game_langton.py` | Simulation | - |
| Safe Cracker | `game_safecracker.py` | SD+ Puzzle | - |
| Slot Machine | `game_slots.py` | SD+ Arcade | - |
| Color Mixer | `game_colormixer.py` | SD+ Puzzle | - |
| DJ Scratch | `game_djscratch.py` | SD+ Music | - |
| Fishing | `game_fishing.py` | SD+ Arcade | - |
| Piano | `game_piano.py` | SD+ Music | - |
| Thermometer | `game_thermometer.py` | SD+ Guess | - |

<!-- [fr] -->
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

<!-- [en] -->

### Arcade

#### Snake

Classic. The snake grows by eating food. Speed increases with score. Wrap-around at edges.

- **Controls**: press any button to turn the snake toward that direction
- **2 players**: two snakes (green/blue) on the same grid. Collision with the other = death

<!-- [fr] -->

### Arcade

#### Snake

Classique. Le serpent grandit en mangeant la nourriture. Vitesse augmente avec le score. Wrap-around aux bords.

- **Contrôles** : appuie n'importe quel bouton pour tourner le serpent vers cette direction
- **2 joueurs** : deux serpents (vert/bleu) sur la même grille. Collision avec l'autre = mort

<!-- [en] -->

#### Breakout

Brick breaker rotated 90 degrees. Bricks on the left, paddle on the right, ball bounces horizontally.

- **Controls**: press the right column to place the paddle, or anywhere to move it
- **Stream Deck +**: the game plays on the touchscreen, the dial moves the paddle; broken bricks may drop items

<!-- [fr] -->

#### Breakout

Casse-briques pivoté 90°. Briques à gauche, paddle à droite, balle rebondit horizontalement.

- **Contrôles** : appuie sur la colonne de droite pour placer le paddle, ou n'importe où pour le déplacer
- **Stream Deck +** : le jeu se joue sur l'écran tactile, le dial déplace le paddle ; les briques cassées lâchent parfois un item

<!-- [en] -->

#### Flappy Bird

The bird moves left to right, obstacles (pipes) scroll. Gravity pulls the bird downward.

- **Controls**: press any button to rise one cell

<!-- [fr] -->

#### Flappy Bird

L'oiseau avance de gauche à droite, les obstacles (tuyaux) défilent. Gravité tire l'oiseau vers le bas.

- **Contrôles** : appuie n'importe quel bouton pour monter d'une case

<!-- [en] -->

#### Pong

Classic Pong rotated 90 degrees. Left paddle vs right paddle. First to 5 points wins.

- **1 player**: left column = you, right = AI
- **2 players**: each deck controls a paddle, press to place it at that line
- **Stream Deck +**: the game plays on the 800x100 touchscreen, a dial moves the paddle, touch places it

<!-- [fr] -->

#### Pong

Pong classique pivoté 90°. Paddle gauche vs paddle droite. Premier à 5 points gagne.

- **1 joueur** : colonne gauche = toi, droite = IA
- **2 joueurs** : chaque deck contrôle un paddle, appuie pour placer à cette ligne
- **Stream Deck +** : le jeu se joue sur l'écran tactile 800x100, un dial déplace le paddle, le toucher le place

<!-- [en] -->

#### Bomberman

Move your character, drop bombs, destroy walls. Don't blow yourself up!

- **Controls**: press adjacent to move, press your position to drop a bomb (3s delay)
- **2 players**: P1 (blue) and P2 (orange) on the same grid. Last alive wins

<!-- [fr] -->

#### Bomberman

Déplace ton personnage, pose des bombes, détruis les murs. Ne te fais pas exploser!

- **Contrôles** : appuie adjacent pour bouger, appuie sur ta position pour poser une bombe (3s de délai)
- **2 joueurs** : P1 (bleu) et P2 (orange) sur la même grille. Dernier vivant gagne

<!-- [en] -->

### Reflex

#### Whack-a-Mole

Moles appear randomly for 30 seconds. Whack them! Speed increases with score. 3 second cooldown at end of game to view score.

- **2 players**: same moles on both decks, separate scores. Highest wins

<!-- [fr] -->

### Réflexe

#### Whack-a-Mole

Des taupes apparaissent aléatoirement pendant 30 secondes. Tape-les! La vitesse augmente avec le score. 3 secondes de cooldown en fin de partie pour voir le score.

- **2 joueurs** : mêmes taupes sur les deux decks, scores séparés. Le plus haut gagne

<!-- [en] -->

#### Reaction Time

A green button lights up after a random delay. Tap it as fast as possible! 5 rounds, time in milliseconds.

- **2 players**: same target, the fastest wins each round. Average compared at the end

<!-- [fr] -->

#### Reaction Time

Un bouton vert s'allume après un délai aléatoire. Tape-le le plus vite possible! 5 rounds, temps en millisecondes.

- **2 joueurs** : même cible, le plus rapide gagne chaque round. Moyenne comparée à la fin

<!-- [en] -->

### Memory

#### Simon Says

The deck plays a light sequence. Reproduce it in order. The sequence grows with each turn.

- **2 players**: same sequence on both decks. First one to make a mistake loses

<!-- [fr] -->

### Mémoire

#### Simon Says

Le deck joue une séquence lumineuse. Reproduis-la dans l'ordre. La séquence s'allonge à chaque tour.

- **2 joueurs** : même séquence sur les deux decks. Le premier à se tromper perd

<!-- [en] -->

#### Color Match

Memory pair game. Flip two cards: if they are the same color, they stay revealed. Find all pairs.

- **2 players**: same board, each flips on their deck. Player with most pairs wins

<!-- [fr] -->

#### Color Match

Jeu de mémoire de paires. Retourne deux cartes : si elles sont de la même couleur, elles restent révélées. Trouve toutes les paires.

- **2 joueurs** : même plateau, chacun retourne sur son deck. Le joueur avec le plus de paires gagne

<!-- [en] -->

### Puzzle

#### Minesweeper

Classic Minesweeper with flag animation (yellow progressive bar on long-press).

- **Controls**: short press = reveal, long press (0.6s) = place/remove flag, press a number = chord (reveal neighbors if flags are correct)
- **2 players (VS Mine Hunter)**: rules reversed! Find mines to score. Mine = +1 + keep your turn. Safe cell = opponent's turn. Flood-fill on empty cells. Player with most mines found wins
- **Parameters**: `-m N` to change mine count, `-v` to display parameters

<!-- [fr] -->

### Puzzle

#### Minesweeper

Démineur classique avec animation de flag (barre jaune progressive en appui long).

- **Contrôles** : appui court = révéler, appui long (0.6s) = poser/retirer drapeau, appui sur chiffre = chord (révéler voisins si drapeaux corrects)
- **2 joueurs (VS Mine Hunter)** : règles inversées! Trouve les mines pour marquer. Mine = +1 + garde ton tour. Case safe = tour de l'adversaire. Flood-fill sur les cases vides. Le joueur avec le plus de mines trouvées gagne
- **Paramètres** : `-m N` pour changer le nombre de mines, `-v` pour afficher les paramètres

<!-- [common] -->

```
.venv/bin/python game_minesweeper.py -m 6   # 6 mines
.venv/bin/python game_minesweeper.py -v     # show params / afficher paramètres
```

<!-- [en] -->

#### Lights Out

Press a button to toggle it and its 4 neighbors. Turn off all lights to win.

- **2 players (coop)**: shared grid! Both players act on the same board

<!-- [fr] -->

#### Lights Out

Appuie un bouton pour le toggle ainsi que ses 4 voisins. Éteins toutes les lumières pour gagner.

- **2 joueurs (coop)** : grille partagée! Les deux joueurs agissent sur le même plateau

<!-- [en] -->

#### 2048

Merge tiles of equal value to reach 2048. Distinct colors per value.

- **Controls**: corners = directions (top-left=up, top-right=right, bottom-left=left, bottom-right=down). Or press the left/right half to go in that direction

<!-- [fr] -->

#### 2048

Fusionne les tuiles de même valeur pour atteindre 2048. Couleurs distinctes par valeur.

- **Contrôles** : coins = directions (haut-gauche=haut, haut-droite=droite, bas-gauche=gauche, bas-droite=bas). Ou appuie la moitié gauche/droite pour aller dans cette direction

<!-- [en] -->

#### Taquin (Sliding Puzzle)

Numbered tiles to put back in order (1->N) by sliding them toward the empty cell. N = number of buttons - 1.

- **Controls**: press a tile adjacent to the empty cell to move it

<!-- [fr] -->

#### Taquin (Sliding Puzzle)

Tuiles numérotées à remettre en ordre (1→N) en les glissant vers la case vide. N = nombre de boutons - 1.

- **Contrôles** : appuie une tuile adjacente à la case vide pour la déplacer

<!-- [en] -->

#### Sokoban

Push boxes (B) onto targets (X). All boxes on targets = victory.

- **Controls**: press adjacent to move. If a box is in front, it gets pushed

<!-- [fr] -->

#### Sokoban

Pousse les boîtes (B) sur les cibles (X). Toutes les boîtes sur les cibles = victoire.

- **Contrôles** : appuie adjacent pour bouger. Si une boîte est devant, elle est poussée

<!-- [en] -->

#### Flood Fill

The grid has random colors. Pick a color in the bottom row to flood-fill from the top-left corner. Fill the whole grid in a limited number of moves.

- **2 players**: same starting grid, each plays independently. First to fill wins

<!-- [fr] -->

#### Flood Fill

La grille a des couleurs aléatoires. Choisis une couleur dans la rangée du bas pour flood-fill depuis le coin haut-gauche. Remplis toute la grille en un nombre limité de coups.

- **2 joueurs** : même grille de départ, chacun joue indépendamment. Premier à remplir gagne

<!-- [en] -->

### Strategy / Deduction

#### Battleship

Naval battle. Ships are hidden. Shoot to find them.

- **1 player**: solo grid, find all ships
- **2 players**: each deck = private attack grid. Hit = keep your turn. Miss = opponent's turn. Sunken ships in dark red. Ships revealed at end of game

<!-- [fr] -->

### Stratégie / Déduction

#### Battleship

Bataille navale. Les bateaux sont cachés. Tire pour les trouver.

- **1 joueur** : grille solo, trouve tous les bateaux
- **2 joueurs** : chaque deck = grille d'attaque privée. Touché = garde ton tour. Manqué = tour de l'adversaire. Bateaux coulés en rouge foncé. Bateaux révélés en fin de partie

<!-- [en] -->

#### Mastermind

Guess the secret color code. Bottom row = your guess (press to cycle colors). Top-right = submit. Feedback after each guess: E = exact (right color, right place), P = partial (right color, wrong place).

<!-- [fr] -->

#### Mastermind

Devine le code secret de couleurs. Rangée du bas = ton essai (appuie pour cycler les couleurs). Haut-droite = soumettre. Feedback après chaque essai : E = exact (bonne couleur, bonne place), P = partiel (bonne couleur, mauvaise place).

<!-- [en] -->

#### Tic-Tac-Toe

Classic noughts and crosses on a 3x3 grid centered on the deck.

- **1 player**: hot seat, players alternate on the same deck
- **2 players**: each deck = one player (X or O). Only the active player's deck accepts input. The other displays "WAIT"

<!-- [fr] -->

#### Tic-Tac-Toe

Morpion classique sur une grille 3x3 centrée sur le deck.

- **1 joueur** : hot seat, les joueurs alternent sur le même deck
- **2 joueurs** : chaque deck = un joueur (X ou O). Seul le deck du joueur actif accepte les inputs. L'autre affiche "WAIT"

<!-- [en] -->

#### Connect 4

Drop pieces in a column; the first to line up 4 wins. The game asks at the start for an AI or a second player.

- **Controls**: press the top row to drop a piece in that column
- **2 players**: on the same deck, or on two decks when both are plugged in

<!-- [fr] -->

#### Connect 4

Lâche des pièces dans une colonne ; le premier à en aligner 4 gagne. Le jeu demande au départ une IA ou un second joueur.

- **Contrôles** : appuie sur la rangée du haut pour lâcher une pièce dans cette colonne
- **2 joueurs** : sur le même deck, ou sur deux decks quand les deux sont branchés

<!-- [en] -->

#### Wordle

Guess a 5-letter word. Bottom row = letters (press to cycle A-Z). Last button = submit. Green = right letter right place, yellow = right letter wrong place, gray = absent. 6 attempts.

<!-- [fr] -->

#### Wordle

Devine un mot de 5 lettres. Rangée du bas = lettres (appuie pour cycler A-Z). Dernier bouton = soumettre. Vert = bonne lettre bonne place, jaune = bonne lettre mauvaise place, gris = absent. 6 essais.

<!-- [en] -->

#### Checkers

Simplified checkers. Select a piece then press the destination. Diagonal moves. Jump to capture.

- **2 players**: red vs blue, each on their own deck

<!-- [fr] -->

#### Checkers

Dames simplifiées. Sélectionne une pièce puis appuie la destination. Déplacements diagonaux. Saute pour capturer.

- **2 joueurs** : rouge vs bleu, chacun son deck

<!-- [en] -->

#### Reversi / Othello

Place pieces to flip the opponent's. Most pieces at the end wins.

- **1 player**: vs AI (simple strategy)
- **2 players**: black vs white

<!-- [fr] -->

#### Reversi / Othello

Place des pièces pour retourner celles de l'adversaire. Le plus de pièces à la fin gagne.

- **1 joueur** : vs IA (stratégie simple)
- **2 joueurs** : noir vs blanc

<!-- [en] -->

### Arcade (continued)

#### Pac-Man

Eat all the dots. Avoid the ghost! Press to change direction. The ghost chases you.

- **Stream Deck +**: the game plays on the touchscreen, the dials steer, a dial press starts

<!-- [fr] -->

### Arcade (suite)

#### Pac-Man

Mange tous les points. Évite le fantôme! Appuie pour changer de direction. Le fantôme te chasse.

- **Stream Deck +** : le jeu se joue sur l'écran tactile, les dials dirigent, un appui sur un dial démarre

<!-- [en] -->

#### Space Invaders

The aliens descend. You are on the bottom row. Press your position to shoot, press adjacent to move.

<!-- [fr] -->

#### Space Invaders

Les aliens descendent. Tu es sur la rangée du bas. Appuie ta position pour tirer, appuie adjacent pour bouger.

<!-- [en] -->

#### Frogger

Cross the road. Cars scroll by. Hop from cell to cell to reach the top!

<!-- [fr] -->

#### Frogger

Traverse la route. Les voitures défilent. Saute de case en case pour atteindre le haut!

<!-- [en] -->

#### Tetris

Pieces fall right to left (rotated 90 degrees). Top row = rotate, bottom = drop, middle = move.

- **Stream Deck +**: the game plays on the touchscreen, the dials control the piece

<!-- [fr] -->

#### Tetris

Pièces tombent de droite à gauche (pivoté 90°). Rangée du haut = rotation, bas = drop, milieu = déplacer.

- **Stream Deck +** : le jeu se joue sur l'écran tactile, les dials contrôlent la pièce

<!-- [en] -->

#### Tower Defense

Enemies cross the middle row. Place towers above/below to take them out. Survive 5 waves!

<!-- [fr] -->

#### Tower Defense

Les ennemis traversent la rangée du milieu. Place des tours au-dessus/en-dessous pour les éliminer. Survie 5 vagues!

<!-- [en] -->

#### Pinball

Vertical pinball: turn the deck 90 degrees so its long side stands up. Keep the ball alive, hit the bumpers, beat your score.

- **Controls**: the right column holds the flippers, top half = left flipper, bottom half = right flipper; press a flipper to launch the ball

<!-- [fr] -->

#### Pinball

Flipper vertical : tourne le deck de 90° pour que son grand côté soit debout. Garde la balle en jeu, touche les bumpers, bats ton score.

- **Contrôles** : la colonne de droite porte les flippers, moitié haute = flipper gauche, moitié basse = flipper droit ; appuie sur un flipper pour lancer la balle

<!-- [en] -->

### Word / Guess

#### Hangman

Each button = a letter. Press to guess. 6 mistakes = game over. The word shows on the top row, or on the touchscreen of a Stream Deck +.

<!-- [fr] -->

### Mot / Devinette

#### Hangman

Chaque bouton = une lettre. Appuie pour deviner. 6 erreurs = game over. Le mot s'affiche sur la rangée du haut, ou sur l'écran tactile d'un Stream Deck +.

<!-- [en] -->

#### Number Guess

Guess a number 1-100. Buttons display values. Colors = hot/cold. Fewer attempts = better score.

<!-- [fr] -->

#### Number Guess

Devine un nombre 1-100. Les boutons affichent des valeurs. Couleurs = chaud/froid. Moins d'essais = meilleur score.

<!-- [en] -->

#### Rock Paper Scissors

3 buttons: rock, paper, scissors. Best of 5.

- **2 players**: simultaneous choice, reveal!

<!-- [fr] -->

#### Rock Paper Scissors

3 boutons : pierre, papier, ciseaux. Best of 5.

- **2 joueurs** : choix simultané, révélation!

<!-- [en] -->

### Puzzle (continued)

#### Sudoku 3x3

Simplified 3x3 grid centered on the deck. Press to cycle digits. No repetitions in rows/columns.

<!-- [fr] -->

### Puzzle (suite)

#### Sudoku 3x3

Grille 3x3 simplifiée centrée sur le deck. Appuie pour cycler les chiffres. Pas de répétitions en lignes/colonnes.

<!-- [en] -->

#### Maze Runner

Randomly generated maze. Navigate from top-left corner to bottom-right. Press adjacent cells to move.

<!-- [fr] -->

#### Maze Runner

Labyrinthe généré aléatoirement. Navigue du coin haut-gauche au bas-droite. Appuie les cases adjacentes pour bouger.

<!-- [en] -->

### Race

#### Top-Down Racer

The road scrolls from right to left. Dodge the obstacles; the speed rises over time. How far can you go?

- **Controls**: press the top or bottom rows to change lane

<!-- [fr] -->

### Course

#### Top-Down Racer

La route défile de droite à gauche. Esquive les obstacles ; la vitesse augmente avec le temps. Jusqu'où iras-tu?

- **Contrôles** : appuie sur les rangées du haut ou du bas pour changer de voie

<!-- [en] -->

#### Drag Race

Shift gears at the right RPM: too early is slow, too late hits the redline. The buttons light up as the RPM rises. Best time wins.

- **Controls**: press when the green zone lights up to shift
- **2 players**: race side by side, one deck each

<!-- [fr] -->

#### Drag Race

Passe les vitesses au bon régime : trop tôt, c'est lent, trop tard, c'est la zone rouge. Les boutons s'allument à mesure que le régime monte. Le meilleur temps gagne.

- **Contrôles** : appuie quand la zone verte s'allume pour passer la vitesse
- **2 joueurs** : course côte à côte, un deck chacun

<!-- [en] -->

### Simulation

#### Game of Life

Conway's cellular automaton. Cells live or die based on their neighbors. Wrap-around at edges.

- **Controls**: press to toggle a cell. Top-left = play/pause. Top-right = randomize. Bottom-right = clear

<!-- [fr] -->

### Simulation

#### Game of Life

Automate cellulaire de Conway. Les cellules vivent ou meurent selon leurs voisins. Wrap-around aux bords.

- **Contrôles** : appuie pour toggle une cellule. Haut-gauche = play/pause. Haut-droite = randomize. Bas-droite = clear

<!-- [en] -->

#### Langton's Ant

Cellular automaton: an ant moves on the grid. On white -> turn right + black. On black -> turn left + white. Emerging patterns!

<!-- [fr] -->

#### Langton's Ant

Automate cellulaire : une fourmi se déplace sur la grille. Sur blanc → tourne à droite + noir. Sur noir → tourne à gauche + blanc. Motifs émergents!

<!-- [en] -->

### Stream Deck + (dials + touchscreen)

#### Safe Cracker

Turn the 4 dials to guess a 4-digit combination. Hot/cold bars on the touchscreen. Click = lock.

<!-- [fr] -->

### Stream Deck + (dials + touchscreen)

#### Safe Cracker

Tourne les 4 dials pour deviner une combinaison 4 chiffres. Barres chaud/froid sur le touchscreen. Click = lock.

<!-- [en] -->

#### Slot Machine

Click a dial to spin all reels. Click each dial to stop its reel. 3 identical = jackpot!

<!-- [fr] -->

#### Slot Machine

Click un dial pour spinner toutes les roues. Click chaque dial pour stopper sa roue. 3 identiques = jackpot!

<!-- [en] -->

#### Color Mixer

3 dials = Red, Green, Blue. Mix to match the target color displayed on the touchscreen. Dial 4 = submit.

<!-- [fr] -->

#### Color Mixer

3 dials = Rouge, Vert, Bleu. Mixe pour matcher la couleur cible affichée sur le touchscreen. Dial 4 = soumettre.

<!-- [en] -->

#### DJ Scratch

Turn the dials to scratch vinyl. Animated waveforms on the touchscreen. Click = change style (sine/square/saw/noise).

<!-- [fr] -->

#### DJ Scratch

Tourne les dials pour scratcher du vinyl. Waveforms animées sur le touchscreen. Click = changer de style (sine/square/saw/noise).

<!-- [en] -->

#### Fishing

Click dial = cast. When the fish bites (touchscreen flash), turn to reel in! Too fast = the line breaks.

<!-- [fr] -->

#### Fishing

Click dial = lancer. Quand le poisson mord (touchscreen flash), tourne pour mouliner! Trop vite = la ligne casse.

<!-- [en] -->

#### Piano

Bottom row = piano keys (C D E F G A B). Dial 1 = change octave. Colors per note on the touchscreen.

<!-- [fr] -->

#### Piano

Rangée du bas = touches de piano (C D E F G A B). Dial 1 = changer d'octave. Couleurs par note sur le touchscreen.

<!-- [en] -->

#### Thermometer

Turn the dial to guess the secret temperature. Thermometer bar on the touchscreen with hot/cold gradient.

<!-- [fr] -->

#### Thermometer

Tourne le dial pour deviner la température secrète. Barre thermomètre sur le touchscreen avec gradient chaud/froid.

<!-- [en] -->

<!-- [en] -->

#### Racing+

Side-scrolling race on the touchscreen. Obstacles scroll from right to left; avoid them and the walls while the speed rises.

- **Controls**: a dial steers up and down

<!-- [fr] -->

#### Racing+

Course à défilement latéral sur l'écran tactile. Les obstacles défilent de droite à gauche ; évite-les, ainsi que les murs, pendant que la vitesse monte.

- **Contrôles** : un dial dirige vers le haut et le bas

<!-- [end] -->
<!-- [en] -->
## Inside ERPLibre

[ERPLibre](https://github.com/ERPLibre/ERPLibre) Home clones this repository
at `script/stream_deck/games/` and follows its `main` branch: a commit
pushed here reaches ERPLibre checkouts at their next update. ERPLibre
launches the games from its TODO menu, `make streamdeck_<id>` and its
GNOME extension's gallery; all three go through its hand-over, which takes
the deck over from its own deck service for the length of the game. Its
`doc/streamdeck_game.md` describes that side; `CONTRACT.md` here states
what both sides expect of each other.

## License

AGPL-3.0 or later, see `LICENSE`.

<!-- [fr] -->
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

<!-- [end] -->
