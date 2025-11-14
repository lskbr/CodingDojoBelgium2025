# Snake Game

A complete implementation of the classic Snake game using Python and PyGame.

## Features

- Grid-based movement
- Snake growth when eating food
- Collision detection (walls and self)
- Score tracking
- Pause functionality
- Game over detection

## Controls

- **Arrow Keys**: Change direction
- **SPACE**: Pause/Resume game
- **R**: Restart game (when game over)
- **ESC**: Quit game

## Running the Game

```bash
python snake.py
```

## Game Rules

- Snake moves continuously in the current direction
- Use arrow keys to change direction
- Eat red food to grow and increase score
- Avoid hitting walls or the snake's own body
- Game ends when snake collides with wall or itself

## Code Structure

- `Snake` class: Handles snake movement, growth, and collision detection
- `Food` class: Handles food positioning and respawning
- `Game` class: Main game loop and state management

## Key Concepts Demonstrated

- Grid-based game mechanics
- Snake body management
- Collision detection
- State management
- Event handling
