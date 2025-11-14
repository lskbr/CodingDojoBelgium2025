"""
Space Invaders Game - Classic Arcade Shooter
A complete implementation of the classic Space Invaders game using PyGame.

Controls:
- Arrow keys: Move ship
- SPACE: Shoot
- ESC: Quit game
- R: Restart game
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
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Game constants
PLAYER_SPEED = 5
BULLET_SPEED = 7
ALIEN_SPEED = 1
ALIEN_DROP_DISTANCE = 30


class Player:
    """Represents the player's ship."""

    def __init__(self):
        self.rect = pygame.Rect(SCREEN_WIDTH // 2 - 25, SCREEN_HEIGHT - 50, 50, 30)
        self.speed = PLAYER_SPEED
        self.bullets = []

    def move_left(self):
        """Move player left."""
        self.rect.x -= self.speed
        if self.rect.x < 0:
            self.rect.x = 0

    def move_right(self):
        """Move player right."""
        self.rect.x += self.speed
        if self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width

    def shoot(self):
        """Create a new bullet."""
        bullet = Bullet(self.rect.centerx, self.rect.top, 1)
        self.bullets.append(bullet)

    def update_bullets(self):
        """Update all player bullets."""
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def draw(self, screen):
        """Draw the player ship."""
        pygame.draw.rect(screen, GREEN, self.rect)
        # Draw ship details
        pygame.draw.polygon(
            screen,
            GREEN,
            [
                (self.rect.centerx, self.rect.top),
                (self.rect.left, self.rect.bottom),
                (self.rect.right, self.rect.bottom),
            ],
        )


class Bullet:
    """Represents a bullet."""

    def __init__(self, x, y, direction):
        self.rect = pygame.Rect(x - 2, y, 4, 10)
        self.speed = BULLET_SPEED
        self.direction = direction  # 1 = up, -1 = down

    def update(self):
        """Update bullet position."""
        self.rect.y -= self.speed * self.direction

    def is_off_screen(self):
        """Check if bullet is off screen."""
        return self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT

    def draw(self, screen, color=WHITE):
        """Draw the bullet."""
        pygame.draw.rect(screen, color, self.rect)


class Alien:
    """Represents an alien."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 20)
        self.speed = ALIEN_SPEED
        self.direction = 1  # 1 = right, -1 = left

    def update(self):
        """Update alien position."""
        self.rect.x += self.speed * self.direction

    def drop_down(self):
        """Drop alien down and reverse direction."""
        self.rect.y += ALIEN_DROP_DISTANCE
        self.direction *= -1

    def draw(self, screen):
        """Draw the alien."""
        pygame.draw.rect(screen, RED, self.rect)
        # Draw alien details
        pygame.draw.circle(screen, WHITE, (self.rect.centerx, self.rect.centery), 5)


class AlienGrid:
    """Manages the grid of aliens."""

    def __init__(self):
        self.aliens = []
        self.direction = 1  # 1 = right, -1 = left
        self.speed = ALIEN_SPEED
        self.drop_distance = ALIEN_DROP_DISTANCE
        self.bullets = []

        # Create grid of aliens
        for row in range(5):
            for col in range(10):
                x = 50 + col * 40
                y = 50 + row * 40
                self.aliens.append(Alien(x, y))

    def update(self):
        """Update all aliens."""
        # Move all aliens
        for alien in self.aliens:
            alien.update()

        # Check if need to drop down
        if self.should_drop():
            for alien in self.aliens:
                alien.drop_down()
            self.direction *= -1  # Reverse direction

        # Random alien shooting
        if self.aliens and random.random() < 0.01:  # 1% chance per frame
            shooter = random.choice(self.aliens)
            bullet = Bullet(shooter.rect.centerx, shooter.rect.bottom, -1)
            self.bullets.append(bullet)

        # Update alien bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)

    def should_drop(self):
        """Check if aliens should drop down."""
        for alien in self.aliens:
            if (alien.rect.right >= SCREEN_WIDTH and self.direction == 1) or (
                alien.rect.left <= 0 and self.direction == -1
            ):
                return True
        return False

    def draw(self, screen):
        """Draw all aliens and their bullets."""
        for alien in self.aliens:
            alien.draw(screen)

        for bullet in self.bullets:
            bullet.draw(screen, YELLOW)


class Game:
    """Main game class."""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Space Invaders")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)

        # Game objects
        self.player = Player()
        self.alien_grid = AlienGrid()

        # Game state
        self.score = 0
        self.lives = 3
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
                elif event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                elif event.key == pygame.K_SPACE and not self.game_over:
                    self.player.shoot()

        return True

    def handle_input(self):
        """Handle continuous input."""
        if not self.game_over:
            keys = pygame.key.get_pressed()

            if keys[pygame.K_LEFT]:
                self.player.move_left()
            if keys[pygame.K_RIGHT]:
                self.player.move_right()

    def update(self):
        """Update game logic."""
        if not self.game_over:
            # Update player bullets
            self.player.update_bullets()

            # Update alien grid
            self.alien_grid.update()

            # Check bullet collisions
            self.check_bullet_collisions()

            # Check if player hit by alien bullet
            for bullet in self.alien_grid.bullets[:]:
                if bullet.rect.colliderect(self.player.rect):
                    self.lives -= 1
                    self.alien_grid.bullets.remove(bullet)
                    if self.lives <= 0:
                        self.game_over = True
                        self.winner = "Aliens"

            # Check if aliens reached bottom
            for alien in self.alien_grid.aliens:
                if alien.rect.bottom >= SCREEN_HEIGHT - 50:
                    self.game_over = True
                    self.winner = "Aliens"

            # Check if all aliens destroyed
            if not self.alien_grid.aliens:
                self.game_over = True
                self.winner = "Player"

    def check_bullet_collisions(self):
        """Check collisions between bullets and aliens."""
        for bullet in self.player.bullets[:]:
            for alien in self.alien_grid.aliens[:]:
                if bullet.rect.colliderect(alien.rect):
                    self.player.bullets.remove(bullet)
                    self.alien_grid.aliens.remove(alien)
                    self.score += 10
                    break

    def draw(self):
        """Draw everything on screen."""
        self.screen.fill(BLACK)

        # Draw stars background
        for i in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            pygame.draw.circle(self.screen, WHITE, (x, y), 1)

        # Draw game objects
        self.player.draw(self.screen)
        self.alien_grid.draw(self.screen)

        # Draw player bullets
        for bullet in self.player.bullets:
            bullet.draw(self.screen)

        # Draw score and lives
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(lives_text, (10, 50))

        # Draw game over message
        if self.game_over:
            if self.winner == "Player":
                game_over_text = self.big_font.render("YOU WIN!", True, GREEN)
            else:
                game_over_text = self.big_font.render("GAME OVER", True, RED)

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

        # Draw controls
        controls_text = self.font.render(
            "Arrow Keys: Move | SPACE: Shoot | ESC: Quit", True, WHITE
        )
        self.screen.blit(controls_text, (10, SCREEN_HEIGHT - 30))

        pygame.display.flip()

    def restart_game(self):
        """Restart the game."""
        self.player = Player()
        self.alien_grid = AlienGrid()
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.winner = None

    def run(self):
        """Main game loop."""
        running = True

        while running:
            # Handle events
            running = self.handle_events()

            # Handle input
            self.handle_input()

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
