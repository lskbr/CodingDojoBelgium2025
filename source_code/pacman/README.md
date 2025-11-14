# Pac-Man Game

A simplified implementation of the classic Pac-Man maze game using Python and PyGame.

For education purposes only.

## Features

- Maze navigation with walls
- Dot collection and scoring
- Power pellets for ghost eating
- Multiple ghosts with basic AI
- Collision detection
- Game over and win conditions

## Controls

- **Arrow Keys**: Move Pac-Man
- **R**: Restart game (when game over)
- **ESC**: Quit game

## Running the Game

```bash
python pacman.py
```

## Game Rules

- Navigate the maze collecting yellow dots
- Avoid ghosts (unless in power mode)
- Collect power pellets to eat ghosts
- Collect all dots to win
- Game ends if Pac-Man touches a ghost (unless in power mode)

## Code Structure

- `Maze` class: Handles maze layout, walls, dots, and power pellets
- `PacMan` class: Handles Pac-Man movement and collision detection
- `Ghost` class: Handles ghost AI and movement
- `Game` class: Main game loop and state management

## Key Concepts Demonstrated

- Maze navigation
- Grid-based movement
- Basic AI pathfinding
- Power-up mechanics
- Game state management

Music by <a href="https://pixabay.com/users/lucadialessandro-25927643/?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=179350">lucadialessandro</a> from <a href="https://pixabay.com//?utm_source=link-attribution&utm_medium=referral&utm_campaign=music&utm_content=179350">Pixabay</a>
