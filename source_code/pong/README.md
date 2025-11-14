# Pong Game

A complete implementation of the classic Pong arcade game using Python and PyGame.

## Features

- Two-player gameplay
- Smooth paddle movement
- Ball physics with speed increase
- Score tracking
- Game over detection
- Restart functionality

## Controls

- **Player 1 (Left Paddle)**: W/S keys
- **Player 2 (Right Paddle)**: Arrow Up/Down keys
- **ESC**: Quit game
- **R**: Restart game (when game over)

## Installation

1. Make sure you have Python 3.7+ installed
2. Install PyGame:
   ```bash
   pip install pygame
   ```

## Running the Game

```bash
python pong.py
```

## Game Rules

- First player to score 5 points wins
- Ball bounces off paddles and top/bottom walls
- Ball speed increases slightly after each paddle hit
- If ball goes off the left side, Player 2 scores
- If ball goes off the right side, Player 1 scores

## Code Structure

- `Paddle` class: Handles paddle movement and drawing
- `Ball` class: Handles ball physics and collision detection
- `Game` class: Main game loop and state management

## Key Concepts Demonstrated

- Game loop architecture
- Event handling
- Collision detection
- Object-oriented programming
- State management
