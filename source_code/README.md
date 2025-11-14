# Classic Games Source Code

This directory contains complete, runnable implementations of 5 classic games using Python and PyGame.

## Games Included

### 1. Pong (`pong/`)

- **File**: `pong.py`
- **Description**: Classic two-player paddle game
- **Features**: Ball physics, scoring, paddle movement
- **Controls**: W/S (Player 1), Arrow Keys (Player 2)

### 2. Snake (`snake/`)

- **File**: `snake.py`
- **Description**: Classic mobile game with growing snake
- **Features**: Grid movement, collision detection, score tracking
- **Controls**: Arrow Keys (move), SPACE (pause)

### 3. Space Invaders (`space_invaders/`)

- **File**: `space_invaders.py`
- **Description**: Classic arcade shooter
- **Features**: Enemy formations, shooting mechanics, lives system
- **Controls**: Arrow Keys (move), SPACE (shoot)

### 4. Pac-Man (`pacman/`)

- **File**: `pacman.py`
- **Description**: Classic maze game
- **Features**: Maze navigation, ghost AI, power pellets
- **Controls**: Arrow Keys (move)

### 5. Super Mario (`super_mario/`)

- **File**: `super_mario.py`
- **Description**: Classic platformer
- **Features**: Platformer physics, scrolling camera, enemies, coins
- **Controls**: Arrow Keys (move), SPACE (jump)

## Installation

1. **Install Python 3.7+** (if not already installed)
2. **Install PyGame**:
   ```bash
   pip install pygame-ce
   ```

## Running the Games

Each game can be run independently:

```bash
# Pong
cd pong
python pong.py

# Snake
cd snake
python snake.py

# Space Invaders
cd space_invaders
python space_invaders.py

# Pac-Man
cd pacman
python pacman.py

# Super Mario
cd super_mario
python super_mario.py
```

## Code Structure

Each game follows a consistent structure:

- **Main game file**: Contains all game logic
- **README.md**: Game-specific documentation
- **Classes**: Organized into logical components (Player, Enemy, etc.)
- **Game loop**: Standard PyGame event handling and rendering

## Key Programming Concepts Demonstrated

### Game Development Fundamentals

- Game loop architecture
- Event handling
- Collision detection
- State management
- Object-oriented programming

### PyGame Specific

- Surface and sprite management
- Input handling (keyboard/mouse)
- Drawing and rendering
- Frame rate control
- Sound and music (in some games)

### Game-Specific Concepts

- **Pong**: Physics simulation, paddle mechanics
- **Snake**: Grid-based movement, body management
- **Space Invaders**: Sprite groups, shooting mechanics
- **Pac-Man**: Maze navigation, AI pathfinding
- **Super Mario**: Platformer physics, camera scrolling

## Educational Value

These games are perfect for learning:

- **Beginners**: Basic Python and PyGame concepts
- **Intermediate**: Game design patterns and architecture
- **Advanced**: Performance optimization and advanced features

## Extending the Games

Each game can be extended with:

- Sound effects and music
- Better graphics and animations
- Additional levels
- Power-ups and special abilities
- Multiplayer functionality
- High score systems

## Troubleshooting

### Common Issues

1. **PyGame not found**: Make sure PyGame is installed (`pip install pygame-ce`)
2. **Display issues**: Try running in windowed mode
3. **Performance**: Reduce frame rate or screen size if needed

### Getting Help

- Check the individual game README files
- Review PyGame documentation
- Check Python and PyGame versions
- Ensure all dependencies are installed

## License

These games are provided for educational purposes. Feel free to use, modify, and learn from the code.
