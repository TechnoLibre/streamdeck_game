
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


### Arcade

#### Snake

Classic. The snake grows by eating food. Speed increases with score. Wrap-around at edges.

- **Controls**: press any button to turn the snake toward that direction
- **2 players**: two snakes (green/blue) on the same grid. Collision with the other = death


#### Breakout

Brick breaker rotated 90 degrees. Bricks on the left, paddle on the right, ball bounces horizontally.

- **Controls**: press the right column to place the paddle, or anywhere to move it
- **Stream Deck +**: the game plays on the touchscreen, the dial moves the paddle; broken bricks may drop items


#### Flappy Bird

The bird moves left to right, obstacles (pipes) scroll. Gravity pulls the bird downward.

- **Controls**: press any button to rise one cell


#### Pong

Classic Pong rotated 90 degrees. Left paddle vs right paddle. First to 5 points wins.

- **1 player**: left column = you, right = AI
- **2 players**: each deck controls a paddle, press to place it at that line
- **Stream Deck +**: the game plays on the 800x100 touchscreen, a dial moves the paddle, touch places it


#### Bomberman

Move your character, drop bombs, destroy walls. Don't blow yourself up!

- **Controls**: press adjacent to move, press your position to drop a bomb (3s delay)
- **2 players**: P1 (blue) and P2 (orange) on the same grid. Last alive wins


### Reflex

#### Whack-a-Mole

Moles appear randomly for 30 seconds. Whack them! Speed increases with score. 3 second cooldown at end of game to view score.

- **2 players**: same moles on both decks, separate scores. Highest wins


#### Reaction Time

A green button lights up after a random delay. Tap it as fast as possible! 5 rounds, time in milliseconds.

- **2 players**: same target, the fastest wins each round. Average compared at the end


### Memory

#### Simon Says

The deck plays a light sequence. Reproduce it in order. The sequence grows with each turn.

- **2 players**: same sequence on both decks. First one to make a mistake loses


#### Color Match

Memory pair game. Flip two cards: if they are the same color, they stay revealed. Find all pairs.

- **2 players**: same board, each flips on their deck. Player with most pairs wins


### Puzzle

#### Minesweeper

Classic Minesweeper with flag animation (yellow progressive bar on long-press).

- **Controls**: short press = reveal, long press (0.6s) = place/remove flag, press a number = chord (reveal neighbors if flags are correct)
- **2 players (VS Mine Hunter)**: rules reversed! Find mines to score. Mine = +1 + keep your turn. Safe cell = opponent's turn. Flood-fill on empty cells. Player with most mines found wins
- **Parameters**: `-m N` to change mine count, `-v` to display parameters


```
.venv/bin/python game_minesweeper.py -m 6   # 6 mines
.venv/bin/python game_minesweeper.py -v     # show params / afficher paramètres
```


#### Lights Out

Press a button to toggle it and its 4 neighbors. Turn off all lights to win.

- **2 players (coop)**: shared grid! Both players act on the same board


#### 2048

Merge tiles of equal value to reach 2048. Distinct colors per value.

- **Controls**: corners = directions (top-left=up, top-right=right, bottom-left=left, bottom-right=down). Or press the left/right half to go in that direction


#### Taquin (Sliding Puzzle)

Numbered tiles to put back in order (1->N) by sliding them toward the empty cell. N = number of buttons - 1.

- **Controls**: press a tile adjacent to the empty cell to move it


#### Sokoban

Push boxes (B) onto targets (X). All boxes on targets = victory.

- **Controls**: press adjacent to move. If a box is in front, it gets pushed


#### Flood Fill

The grid has random colors. Pick a color in the bottom row to flood-fill from the top-left corner. Fill the whole grid in a limited number of moves.

- **2 players**: same starting grid, each plays independently. First to fill wins


### Strategy / Deduction

#### Battleship

Naval battle. Ships are hidden. Shoot to find them.

- **1 player**: solo grid, find all ships
- **2 players**: each deck = private attack grid. Hit = keep your turn. Miss = opponent's turn. Sunken ships in dark red. Ships revealed at end of game


#### Mastermind

Guess the secret color code. Bottom row = your guess (press to cycle colors). Top-right = submit. Feedback after each guess: E = exact (right color, right place), P = partial (right color, wrong place).


#### Tic-Tac-Toe

Classic noughts and crosses on a 3x3 grid centered on the deck.

- **1 player**: hot seat, players alternate on the same deck
- **2 players**: each deck = one player (X or O). Only the active player's deck accepts input. The other displays "WAIT"


#### Connect 4

Drop pieces in a column; the first to line up 4 wins. The game asks at the start for an AI or a second player.

- **Controls**: press the top row to drop a piece in that column
- **2 players**: on the same deck, or on two decks when both are plugged in


#### Wordle

Guess a 5-letter word. Bottom row = letters (press to cycle A-Z). Last button = submit. Green = right letter right place, yellow = right letter wrong place, gray = absent. 6 attempts.


#### Checkers

Simplified checkers. Select a piece then press the destination. Diagonal moves. Jump to capture.

- **2 players**: red vs blue, each on their own deck


#### Reversi / Othello

Place pieces to flip the opponent's. Most pieces at the end wins.

- **1 player**: vs AI (simple strategy)
- **2 players**: black vs white


### Arcade (continued)

#### Pac-Man

Eat all the dots. Avoid the ghost! Press to change direction. The ghost chases you.

- **Stream Deck +**: the game plays on the touchscreen, the dials steer, a dial press starts


#### Space Invaders

The aliens descend. You are on the bottom row. Press your position to shoot, press adjacent to move.


#### Frogger

Cross the road. Cars scroll by. Hop from cell to cell to reach the top!


#### Tetris

Pieces fall right to left (rotated 90 degrees). Top row = rotate, bottom = drop, middle = move.

- **Stream Deck +**: the game plays on the touchscreen, the dials control the piece


#### Tower Defense

Enemies cross the middle row. Place towers above/below to take them out. Survive 5 waves!


#### Pinball

Vertical pinball: turn the deck 90 degrees so its long side stands up. Keep the ball alive, hit the bumpers, beat your score.

- **Controls**: the right column holds the flippers, top half = left flipper, bottom half = right flipper; press a flipper to launch the ball


### Word / Guess

#### Hangman

Each button = a letter. Press to guess. 6 mistakes = game over. The word shows on the top row, or on the touchscreen of a Stream Deck +.


#### Number Guess

Guess a number 1-100. Buttons display values. Colors = hot/cold. Fewer attempts = better score.


#### Rock Paper Scissors

3 buttons: rock, paper, scissors. Best of 5.

- **2 players**: simultaneous choice, reveal!


### Puzzle (continued)

#### Sudoku 3x3

Simplified 3x3 grid centered on the deck. Press to cycle digits. No repetitions in rows/columns.


#### Maze Runner

Randomly generated maze. Navigate from top-left corner to bottom-right. Press adjacent cells to move.


### Race

#### Top-Down Racer

The road scrolls from right to left. Dodge the obstacles; the speed rises over time. How far can you go?

- **Controls**: press the top or bottom rows to change lane


#### Drag Race

Shift gears at the right RPM: too early is slow, too late hits the redline. The buttons light up as the RPM rises. Best time wins.

- **Controls**: press when the green zone lights up to shift
- **2 players**: race side by side, one deck each


### Simulation

#### Game of Life

Conway's cellular automaton. Cells live or die based on their neighbors. Wrap-around at edges.

- **Controls**: press to toggle a cell. Top-left = play/pause. Top-right = randomize. Bottom-right = clear


#### Langton's Ant

Cellular automaton: an ant moves on the grid. On white -> turn right + black. On black -> turn left + white. Emerging patterns!


### Stream Deck + (dials + touchscreen)

#### Safe Cracker

Turn the 4 dials to guess a 4-digit combination. Hot/cold bars on the touchscreen. Click = lock.


#### Slot Machine

Click a dial to spin all reels. Click each dial to stop its reel. 3 identical = jackpot!


#### Color Mixer

3 dials = Red, Green, Blue. Mix to match the target color displayed on the touchscreen. Dial 4 = submit.


#### DJ Scratch

Turn the dials to scratch vinyl. Animated waveforms on the touchscreen. Click = change style (sine/square/saw/noise).


#### Fishing

Click dial = cast. When the fish bites (touchscreen flash), turn to reel in! Too fast = the line breaks.


#### Piano

Bottom row = piano keys (C D E F G A B). Dial 1 = change octave. Colors per note on the touchscreen.


#### Thermometer

Turn the dial to guess the secret temperature. Thermometer bar on the touchscreen with hot/cold gradient.



#### Racing+

Side-scrolling race on the touchscreen. Obstacles scroll from right to left; avoid them and the walls while the speed rises.

- **Controls**: a dial steers up and down

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
