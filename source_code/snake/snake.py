"""
Snake Game - Classic Mobile Game
A complete implementation of the classic Snake game using PyGame.

Controls:
- Arrow keys: Change direction
- ESC: Quit game
- R: Restart game
"""

import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 600
FPS = 10

# Grid settings
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
DARK_GREEN = (0, 150, 0)


class Snake:
    """Represents the snake in the game."""

    def __init__(self):
        self.body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)  # Moving right
        self.grow = False

    def move(self):
        """Move the snake in the current direction."""
        head_x, head_y = self.body[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])

        self.body.insert(0, new_head)

        if not self.grow:
            self.body.pop()  # Remove tail
        else:
            self.grow = False

    def change_direction(self, new_direction):
        """Change snake direction (prevent moving backwards)."""
        # Prevent moving backwards into self
        if (new_direction[0] * -1, new_direction[1] * -1) != self.direction:
            self.direction = new_direction

    def grow_snake(self):
        """Make the snake grow on next move."""
        self.grow = True

    def check_collision(self):
        """Check if snake collides with walls or itself."""
        head = self.body[0]

        # Check wall collision
        if (
            head[0] < 0
            or head[0] >= GRID_WIDTH
            or head[1] < 0
            or head[1] >= GRID_HEIGHT
        ):
            return True

        # Check self collision
        if head in self.body[1:]:
            return True

        return False

    def draw(self, screen):
        """Draw the snake on screen."""
        for i, segment in enumerate(self.body):
            x = segment[0] * GRID_SIZE
            y = segment[1] * GRID_SIZE

            # Head is brighter
            color = GREEN if i == 0 else DARK_GREEN
            pygame.draw.rect(screen, color, (x, y, GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BLACK, (x, y, GRID_SIZE, GRID_SIZE), 1)


class Food:
    """Represents the food in the game."""

    def __init__(self):
        self.position = self.generate_position()

    def generate_position(self):
        """Generate a random position for food."""
        x = random.randint(0, GRID_WIDTH - 1)
        y = random.randint(0, GRID_HEIGHT - 1)
        return (x, y)

    def respawn(self, snake_body):
        """Respawn food in a new position (not on snake)."""
        while True:
            self.position = self.generate_position()
            if self.position not in snake_body:
                break

    def draw(self, screen):
        """Draw the food on screen."""
        x = self.position[0] * GRID_SIZE
        y = self.position[1] * GRID_SIZE
        pygame.draw.rect(screen, RED, (x, y, GRID_SIZE, GRID_SIZE))


class Game:
    """Main game class."""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)

        # Game objects
        self.snake = Snake()
        self.food = Food()

        # Game state
        self.score = 0
        self.game_over = False
        self.paused = False

    def handle_events(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_SPACE and not self.game_over:
                    self.paused = not self.paused
                elif not self.game_over and not self.paused:
                    # Handle direction changes
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
        return True

    def update(self):
        """Update game logic."""
        if not self.game_over and not self.paused:
            self.snake.move()

            # Check collisions
            if self.snake.check_collision():
                self.game_over = True
                return

            # Check food collision
            if self.snake.body[0] == self.food.position:
                self.snake.grow_snake()
                self.score += 10
                self.food.respawn(self.snake.body)

    def draw(self):
        """Draw everything on screen."""
        self.screen.fill(BLACK)

        # Draw snake and food
        self.snake.draw(self.screen)
        self.food.draw(self.screen)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

        # Draw game over message
        if self.game_over:
            game_over_text = self.big_font.render("GAME OVER", True, WHITE)
            text_rect = game_over_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            self.screen.blit(game_over_text, text_rect)

            restart_text = self.font.render(
                "Press R to restart or ESC to quit", True, WHITE
            )
            restart_rect = restart_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            )
            self.screen.blit(restart_text, restart_rect)

        # Draw pause message
        if self.paused and not self.game_over:
            pause_text = self.big_font.render("PAUSED", True, WHITE)
            text_rect = pause_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            self.screen.blit(pause_text, text_rect)

            resume_text = self.font.render("Press SPACE to resume", True, WHITE)
            resume_rect = resume_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            )
            self.screen.blit(resume_text, resume_rect)

        # Draw controls
        controls_text = self.font.render(
            "Arrow Keys: Move | SPACE: Pause | ESC: Quit", True, WHITE
        )
        self.screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))

        pygame.display.flip()

    def restart_game(self):
        """Restart the game."""
        self.snake = Snake()
        self.food = Food()
        self.score = 0
        self.game_over = False
        self.paused = False

    def run(self):
        """Main game loop."""
        running = True

        while running:
            # Handle events
            running = self.handle_events()

            # Update game
            self.update()

            # Draw everything
            self.draw()

            # Control frame rate
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Main function."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
