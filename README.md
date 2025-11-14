# CoderDojo Classic Games Programming Presentation

A comprehensive presentation about classic games programming using Python and PyGame, designed for beginners who already know Python basics.

## Overview

This presentation covers:

- Introduction to game programming and PyGame
- Core game programming concepts
- 4 classic games: Pong, Snake, Space Invaders, Pac-Man.

## Setup Requirements

**Installation steps:**

```bash
# Install Python (if not already installed)
# Download from https://python.org

# Install PyGame - use a virtual environment!
pip install pygame-ce

# Verify installation
python -c "import pygame; print('PyGame installed successfully!')"
```

### For Live Coding Demos

**Recommended setup:**

1. Have a simple game template ready
2. Use a large font size in your code editor
3. Have the presentation slides open in a separate window
4. Practice the code examples beforehand

**Demo game template:**

```python
import pygame

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Create screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game Demo")
clock = pygame.time.Clock()

# Game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Update game logic
    # (Add your game logic here)

    # Draw everything
    screen.fill(BLACK)
    # (Add your drawing code here)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
```

## Additional Resources

### Documentation

- [PyGame Documentation](https://www.pygame.org/docs/)
- [Python Game Programming](https://pythonprogramming.net/pygame-python-3-part-1-intro/)
- [Game Development Tutorials](https://realpython.com/pygame-a-primer/)

### Community

- [PyGame Reddit](https://reddit.com/r/pygame)
- [Game Development Discord](https://discord.gg/gamedev)
- [Stack Overflow PyGame Tag](https://stackoverflow.com/questions/tagged/pygame)

### Tools

- [Aseprite](https://aseprite.org/) - Pixel art editor
- [Tiled](https://www.mapeditor.org/) - Tile map editor
- [Audacity](https://audacityteam.org/) - Audio editor

## License

This presentation is provided for educational purposes. Feel free to use and modify for your own CoderDojo sessions.

## Contributing

If you have suggestions for improving this presentation:

1. Fork the repository
2. Make your changes
3. Submit a pull request

## Contact

For questions about this presentation or CoderDojo resources, please contact [questions@pythonfromscratch.com].
