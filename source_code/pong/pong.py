"""
Pong Game - Classic Arcade Game
A complete implementation of the classic Pong game using PyGame.

Controls:
- Player 1 (Left): W/S keys
- Player 2 (Right): Arrow Up/Down keys
- ESC: Quit game
"""

import pygame
import sys
import random

# Initialize PyGame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)

# Game constants
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 80
PADDLE_SPEED = 5
BALL_SIZE = 15
BALL_SPEED = 4
SCORE_LIMIT = 5


class Paddle:
    """Represents a paddle in the Pong game."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = PADDLE_SPEED

    def move_up(self):
        """Move paddle up."""
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.rect.y = 0

    def move_down(self):
        """Move paddle down."""
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT - PADDLE_HEIGHT:
            self.rect.y = SCREEN_HEIGHT - PADDLE_HEIGHT

    def draw(self, screen):
        """Draw the paddle on screen."""
        pygame.draw.rect(screen, WHITE, self.rect)


class Ball:
    """Represents the ball in the Pong game."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED * random.choice([-1, 1])
        self.speed_y = BALL_SPEED * random.choice([-1, 1])
        self.original_speed = BALL_SPEED

    def update(self):
        """Update ball position."""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

    def bounce_y(self):
        """Bounce ball off top/bottom walls."""
        self.speed_y = -self.speed_y

    def bounce_x(self):
        """Bounce ball off paddles."""
        self.speed_x = -self.speed_x
        # Increase speed slightly
        self.speed_x *= 1.1
        self.speed_y *= 1.1

    def reset(self):
        """Reset ball to center with random direction."""
        self.rect.x = SCREEN_WIDTH // 2 - BALL_SIZE // 2
        self.rect.y = SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        self.speed_x = self.original_speed * random.choice([-1, 1])
        self.speed_y = self.original_speed * random.choice([-1, 1])

    def draw(self, screen):
        """Draw the ball on screen."""
        pygame.draw.rect(screen, WHITE, self.rect)


class Game:
    """Main game class."""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pong - Classic Arcade Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

        # Game objects
        self.left_paddle = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.right_paddle = Paddle(
            SCREEN_WIDTH - 50 - PADDLE_WIDTH, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        )
        self.ball = Ball(
            SCREEN_WIDTH // 2 - BALL_SIZE // 2, SCREEN_HEIGHT // 2 - BALL_SIZE // 2
        )

        # Game state
        self.left_score = 0
        self.right_score = 0
        self.game_over = False
        self.winner = None

    def handle_events(self):
        """Handle user input."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
        return True

    def handle_input(self):
        """Handle continuous input."""
        keys = pygame.key.get_pressed()

        # Left paddle (Player 1) - W/S keys
        if keys[pygame.K_w]:
            self.left_paddle.move_up()
        if keys[pygame.K_s]:
            self.left_paddle.move_down()

        # Right paddle (Player 2) - Arrow keys
        if keys[pygame.K_UP]:
            self.right_paddle.move_up()
        if keys[pygame.K_DOWN]:
            self.right_paddle.move_down()

    def update_ball(self):
        """Update ball physics and collisions."""
        if not self.game_over:
            self.ball.update()

            # Bounce off top/bottom walls
            if self.ball.rect.top <= 0 or self.ball.rect.bottom >= SCREEN_HEIGHT:
                self.ball.bounce_y()

            # Bounce off paddles
            if self.ball.rect.colliderect(self.left_paddle.rect):
                self.ball.bounce_x()
                # Ensure ball moves right
                if self.ball.speed_x < 0:
                    self.ball.speed_x = -self.ball.speed_x

            if self.ball.rect.colliderect(self.right_paddle.rect):
                self.ball.bounce_x()
                # Ensure ball moves left
                if self.ball.speed_x > 0:
                    self.ball.speed_x = -self.ball.speed_x

            # Check for scoring
            if self.ball.rect.left <= 0:
                self.right_score += 1
                self.ball.reset()
                if self.right_score >= SCORE_LIMIT:
                    self.game_over = True
                    self.winner = "Player 2"

            if self.ball.rect.right >= SCREEN_WIDTH:
                self.left_score += 1
                self.ball.reset()
                if self.left_score >= SCORE_LIMIT:
                    self.game_over = True
                    self.winner = "Player 1"

    def draw(self):
        """Draw everything on screen."""
        self.screen.fill(BLACK)

        # Draw center line
        for y in range(0, SCREEN_HEIGHT, 20):
            pygame.draw.rect(self.screen, GRAY, (SCREEN_WIDTH // 2 - 2, y, 4, 10))

        # Draw paddles and ball
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)

        # Draw scores
        left_text = self.font.render(str(self.left_score), True, WHITE)
        right_text = self.font.render(str(self.right_score), True, WHITE)
        self.screen.blit(left_text, (SCREEN_WIDTH // 4, 50))
        self.screen.blit(right_text, (3 * SCREEN_WIDTH // 4, 50))

        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render(f"{self.winner} Wins!", True, WHITE)
            text_rect = game_over_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            self.screen.blit(game_over_text, text_rect)

            restart_text = self.small_font.render(
                "Press R to restart or ESC to quit", True, WHITE
            )
            restart_rect = restart_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            )
            self.screen.blit(restart_text, restart_rect)

        # Draw controls
        controls_text = self.small_font.render(
            "Player 1: W/S | Player 2: Arrow Keys", True, GRAY
        )
        self.screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))

        pygame.display.flip()

    def restart_game(self):
        """Restart the game."""
        self.left_score = 0
        self.right_score = 0
        self.game_over = False
        self.winner = None
        self.ball.reset()
        self.left_paddle.rect.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2
        self.right_paddle.rect.y = SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2

    def run(self):
        """Main game loop."""
        running = True

        while running:
            # Handle events
            running = self.handle_events()

            # Handle restart
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r] and self.game_over:
                self.restart_game()

            if not self.game_over:
                # Handle input
                self.handle_input()

                # Update game
                self.update_ball()

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
