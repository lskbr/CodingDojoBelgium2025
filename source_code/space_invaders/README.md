# Space Invaders Game

A complete implementation of the classic Space Invaders arcade game using Python and PyGame.

## Features

- Player ship with shooting mechanics
- Grid of aliens with movement patterns
- Collision detection between bullets and aliens
- Score tracking and lives system
- Progressive difficulty
- Game over detection

## Controls

- **Arrow Keys**: Move ship left/right
- **SPACE**: Shoot bullets
- **R**: Restart game (when game over)
- **ESC**: Quit game

## Running the Game

```bash
python space_invaders.py
```

## Game Rules

- Destroy all aliens to win
- Avoid alien bullets
- Aliens move in formation and drop down when hitting edges
- Aliens shoot back at random intervals
- Game ends when all aliens are destroyed or player loses all lives

## Code Structure

- `Player` class: Handles player ship movement and shooting
- `Bullet` class: Handles bullet physics and rendering
- `Alien` class: Individual alien behavior
- `AlienGrid` class: Manages the formation of aliens
- `Game` class: Main game loop and state management

## Key Concepts Demonstrated

- Sprite groups and management
- Collision detection
- Random events
- Game state management
- Shooting mechanics
