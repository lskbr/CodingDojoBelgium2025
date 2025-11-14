"""
Pac-Man Game - Classic Maze Game
A simplified implementation of the classic Pac-Man game using PyGame.

Controls:
- Arrow keys: Move Pac-Man
- ESC: Quit game
- R: Restart game
"""

import pygame
import sys
import random
import os

# Initialize PyGame
pygame.init()
pygame.mixer.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 840  # Extra space for score display
FPS = 30  # Target frame rate (game is frame-rate independent)
GRID_WIDTH = 20
GRID_HEIGHT = 20
CELL_SIZE = min(SCREEN_WIDTH // GRID_WIDTH, (SCREEN_HEIGHT - 40) // GRID_HEIGHT)
SCORE_HEIGHT = 40

# Colors
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
PINK = (255, 192, 203)
CYAN = (0, 255, 255)
ORANGE = (255, 165, 0)
GREEN = (0, 255, 0)

# Game speeds (in pixels per second for frame-rate independence)
PACMAN_SPEED = 120  # pixels per second (2 pixels/frame at 60 FPS)
GHOST_SPEED = 72  # pixels per second (1.2 pixels/frame at 60 FPS)
GHOST_SPEED_VARIATION = 0.1  # 10% random speed variation per ghost

# Power-up duration
POWER_UP_DURATION = 5.0  # seconds

# Game states
STATE_PLAYING = 0
STATE_GAME_OVER = 1
STATE_WON = 2

# CELL x CELL Maze
# X is a WALL
# S is pacman's start position
# G is a ghost's start position
# P is a power pellet
MAZE = """
XXXXXXXX.XXXXXXXXXXX
XS...X......X......X
X.XX.X.XXXX.X.XXXX.X
X.P..............P.X
X.XXXX.X.XX.X.XXXX.X
X......X....X......X
X.XXXX.X.XX.X.XXXX.X
X..................X
XX.XX.XXXXXX.XX.XXGX
.......G.P..........
XX.XX.XXXXXX.XX.XXGX
X..................X
X.XXXX.X.XX.X.XXXX.X
X......X....X......X
X.XXXX.X.XX.X.XXXX.X
X.P  ..........  P.X
X.X.XX.XXXX.XXX.XXXX
XGX.XX.X..X.....X..X
X ...........XX    X
XXXXXXXX.XXXXXXXXXXX
"""


class Wall(pygame.sprite.Sprite):
    """Wall sprite - blocks movement"""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((CELL_SIZE, CELL_SIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y + SCORE_HEIGHT


class Pellet(pygame.sprite.Sprite):
    """Regular pellet - gives points when eaten"""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x + CELL_SIZE // 2
        self.rect.centery = y + CELL_SIZE // 2 + SCORE_HEIGHT
        self.points = 10


class PowerPellet(pygame.sprite.Sprite):
    """Power pellet - gives points and makes ghosts vulnerable"""

    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((12, 12))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.centerx = x + CELL_SIZE // 2
        self.rect.centery = y + CELL_SIZE // 2 + SCORE_HEIGHT
        self.points = 50


class Pacman(pygame.sprite.Sprite):
    """Pacman sprite - player controlled character"""

    def __init__(self, x, y):
        super().__init__()
        self.size = CELL_SIZE - 10  # Make pacman smaller
        self.base_image = None
        self.image = None
        self.rect = None
        self.create_pacman_image(mouth_open=True)
        self.rect.x = x + 5
        self.rect.y = y + 5 + SCORE_HEIGHT
        self.start_x = x + 5
        self.start_y = y + 5
        self.dx = 0
        self.dy = 0
        self.next_dx = 0
        self.next_dy = 0
        self.mouth_open = True
        self.mouth_timer = 0

    def create_pacman_image(self, mouth_open=True):
        """Create pacman sprite that looks like a pizza slice"""
        size = self.size
        # Create surface with transparency
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # Transparent background

        center = size // 2
        radius = size // 2

        if mouth_open:
            # Draw pacman with mouth open (missing slice)
            # Draw the circle with a pie slice missing
            pygame.draw.circle(surface, YELLOW, (center, center), radius)

            # Cut out the mouth triangle (missing pizza slice)
            mouth_points = [
                (center, center),
                (center + radius * 1.5, center - radius * 0.6),
                (center + radius * 1.5, center + radius * 0.6),
            ]
            pygame.draw.polygon(surface, (0, 0, 0, 0), mouth_points)
        else:
            # Draw closed mouth (full circle)
            pygame.draw.circle(surface, YELLOW, (center, center), radius)

        # Draw eye (black dot)
        eye_x = center - radius // 3
        eye_y = center - radius // 3
        pygame.draw.rect(surface, BLACK, (eye_x, eye_y, 4, 4))

        self.base_image = surface
        self.image = self.base_image.copy()
        if self.rect is None:
            self.rect = self.image.get_rect()

    def update(self, walls, dt=0):
        """Update Pacman position with collision detection"""
        # Update mouth animation
        self.mouth_timer += dt
        if self.mouth_timer >= 0.1:
            self.mouth_timer = 0
            self.mouth_open = not self.mouth_open
            self.create_pacman_image(self.mouth_open)
            # Update rotation/flip based on direction
            old_center = self.rect.center

            if self.dx > 0:
                # Right - use original image
                self.image = self.base_image.copy()
            elif self.dx < 0:
                # Left - flip horizontally instead of rotating
                self.image = pygame.transform.flip(self.base_image, True, False)
            elif self.dy > 0:
                # Down - rotate 270 degrees
                self.image = pygame.transform.rotate(self.base_image, 270)
            elif self.dy < 0:
                # Up - rotate 90 degrees
                self.image = pygame.transform.rotate(self.base_image, 90)
            else:
                # Not moving - use original
                self.image = self.base_image.copy()

            # Update rect to maintain position after transformation
            self.rect = self.image.get_rect()
            self.rect.center = old_center

        # Try to change direction if a new direction was requested
        if self.next_dx != 0 or self.next_dy != 0:
            test_x = self.rect.x + self.next_dx * PACMAN_SPEED * dt
            test_y = self.rect.y + self.next_dy * PACMAN_SPEED * dt

            # Create a test rect to check collision
            test_rect = self.rect.copy()
            test_rect.x = test_x
            test_rect.y = test_y

            # Check if the new direction is valid
            collision = False
            for wall in walls:
                if test_rect.colliderect(wall.rect):
                    collision = True
                    break

            if not collision:
                self.dx = self.next_dx
                self.dy = self.next_dy
                self.next_dx = 0
                self.next_dy = 0

        # Move in current direction (frame-rate independent)
        if self.dx != 0 or self.dy != 0:
            new_x = self.rect.x + self.dx * PACMAN_SPEED * dt
            new_y = self.rect.y + self.dy * PACMAN_SPEED * dt

            # Create a test rect
            test_rect = self.rect.copy()
            test_rect.x = new_x
            test_rect.y = new_y

            # Check collision with walls
            collision = False
            for wall in walls:
                if test_rect.colliderect(wall.rect):
                    collision = True
                    break

            if not collision:
                self.rect.x = new_x
                self.rect.y = new_y
            else:
                # Stop if hit a wall
                self.dx = 0
                self.dy = 0

        # Check for wraparound at maze edges (teleport to opposite side)
        # The playable maze is from y=SCORE_HEIGHT to y=SCORE_HEIGHT+maze_height
        maze_width = GRID_WIDTH * CELL_SIZE
        maze_height = GRID_HEIGHT * CELL_SIZE

        # Horizontal wraparound
        if self.rect.right < 0:  # Gone off left edge
            self.rect.x = maze_width
        elif self.rect.left > maze_width:  # Gone off right edge
            self.rect.x = -self.rect.width

        # Vertical wraparound (score area is NOT part of the playable maze)
        if self.rect.top < SCORE_HEIGHT:  # Gone into/above score area (top of screen)
            self.rect.y = maze_height + SCORE_HEIGHT - self.rect.height
        elif self.rect.top > maze_height + SCORE_HEIGHT:  # Gone off bottom edge
            self.rect.y = SCORE_HEIGHT

    def set_direction(self, dx, dy):
        """Set the next direction to move"""
        self.next_dx = dx
        self.next_dy = dy

    def reset(self):
        """Reset Pacman to starting position"""
        self.rect.x = self.start_x
        self.rect.y = self.start_y + SCORE_HEIGHT
        self.dx = 0
        self.dy = 0
        self.next_dx = 0
        self.next_dy = 0
        self.mouth_open = True
        self.mouth_timer = 0


class Ghost(pygame.sprite.Sprite):
    """Ghost sprite - enemy that chases Pacman"""

    def __init__(self, x, y, color):
        super().__init__()
        self.size = CELL_SIZE - 4
        self.color = color
        self.original_color = color
        self.vulnerable_colors = [BLUE, WHITE, YELLOW]
        self.color_index = 0
        self.color_timer = 0
        # Add random speed variation (up to 5%)
        speed_multiplier = 1.0 + random.uniform(0, GHOST_SPEED_VARIATION)
        self.speed = GHOST_SPEED * speed_multiplier
        self.image = self.create_ghost_image(color)
        self.rect = self.image.get_rect()
        self.rect.x = x + 2
        self.rect.y = y + 2 + SCORE_HEIGHT
        self.start_x = x + 2
        self.start_y = y + 2
        self.dx = random.choice([-1, 1])
        self.dy = 0

    def create_ghost_image(self, color):
        """Create a ghost sprite with rounded top and wavy bottom"""
        size = self.size
        surface = pygame.Surface((size, size), pygame.SRCALPHA)
        surface.fill((0, 0, 0, 0))  # Transparent background

        # Draw the ghost body
        # Top half - rounded dome
        top_height = size // 2
        for y in range(top_height):
            # Create rounded top using a semicircle approximation
            width_at_y = int(size * (1 - (1 - y / top_height) ** 2) ** 0.5)
            left_x = (size - width_at_y) // 2
            if width_at_y > 0:
                pygame.draw.rect(surface, color, (left_x, y, width_at_y, 1))

        # Middle section - full width rectangle
        pygame.draw.rect(surface, color, (0, top_height, size, size // 2))

        # Bottom - wavy edge (three bumps)
        wave_height = size // 6
        bump_width = size // 3
        for i in range(3):
            center_x = bump_width * i + bump_width // 2
            center_y = size - wave_height // 2
            pygame.draw.circle(surface, color, (center_x, center_y), bump_width // 2)

        # Draw eyes (two white circles with black pupils)
        eye_y = size // 3
        eye_size = size // 6
        pupil_size = eye_size // 2

        # Left eye
        left_eye_x = size // 3
        pygame.draw.circle(surface, WHITE, (left_eye_x, eye_y), eye_size)
        pygame.draw.circle(surface, BLACK, (left_eye_x, eye_y), pupil_size)

        # Right eye
        right_eye_x = 2 * size // 3
        pygame.draw.circle(surface, WHITE, (right_eye_x, eye_y), eye_size)
        pygame.draw.circle(surface, BLACK, (right_eye_x, eye_y), pupil_size)

        return surface

    def update(self, walls, pacman, vulnerable=False, dt=0):
        """Update ghost position with AI - chase when normal, flee when vulnerable"""
        # Update color cycling if vulnerable
        if vulnerable:
            self.color_timer += dt
            if self.color_timer >= 0.2:  # Change color every 0.2 seconds
                self.color_timer = 0
                self.color_index = (self.color_index + 1) % len(self.vulnerable_colors)
                self.color = self.vulnerable_colors[self.color_index]
                self.image = self.create_ghost_image(self.color)
        else:
            # Reset to original color when not vulnerable
            if self.color != self.original_color:
                self.color = self.original_color
                self.image = self.create_ghost_image(self.original_color)
                self.color_timer = 0
                self.color_index = 0

        # Determine desired direction based on vulnerable state
        # All possible directions: up, down, left, right
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # Up  # Down  # Left  # Right

        # Score each direction based on whether we want to chase or flee
        best_direction = None
        best_score = None

        for dx, dy in directions:
            # Test if we can move in this direction (use fixed lookahead distance)
            test_rect = self.rect.copy()
            lookahead_distance = 4  # pixels
            test_rect.x = self.rect.x + dx * lookahead_distance
            test_rect.y = self.rect.y + dy * lookahead_distance

            # Check for wall collision
            collision = False
            for wall in walls:
                if test_rect.colliderect(wall.rect):
                    collision = True
                    break

            if not collision:
                # Calculate what the distance to Pacman would be if we move this way
                # Use fixed lookahead for AI decisions
                future_lookahead = 15  # pixels
                future_x = self.rect.centerx + dx * future_lookahead
                future_y = self.rect.centery + dy * future_lookahead
                distance_after_move = (
                    (future_x - pacman.rect.centerx) ** 2
                    + (future_y - pacman.rect.centery) ** 2
                ) ** 0.5

                if vulnerable:
                    # When vulnerable, prefer directions that increase distance (flee)
                    score = distance_after_move
                else:
                    # When not vulnerable, prefer directions that decrease distance (chase)
                    score = -distance_after_move

                # Prefer to keep moving in current direction (add small bonus)
                if dx == self.dx and dy == self.dy:
                    score += 5

                if best_score is None or score > best_score:
                    best_score = score
                    best_direction = (dx, dy)

        # Update direction if we found a valid one
        if best_direction:
            self.dx, self.dy = best_direction

        # Move in current direction (frame-rate independent)
        new_x = self.rect.x + self.dx * self.speed * dt
        new_y = self.rect.y + self.dy * self.speed * dt

        test_rect = self.rect.copy()
        test_rect.x = new_x
        test_rect.y = new_y

        # Check collision
        collision = False
        for wall in walls:
            if test_rect.colliderect(wall.rect):
                collision = True
                break

        if not collision:
            self.rect.x = new_x
            self.rect.y = new_y
        else:
            # Hit a wall, force recalculation on next update
            # Try to find any valid direction (use fixed lookahead)
            random.shuffle(directions)
            for dx, dy in directions:
                test_rect = self.rect.copy()
                lookahead_distance = 6  # pixels
                test_rect.x = self.rect.x + dx * lookahead_distance
                test_rect.y = self.rect.y + dy * lookahead_distance

                collision = False
                for wall in walls:
                    if test_rect.colliderect(wall.rect):
                        collision = True
                        break

                if not collision:
                    self.dx = dx
                    self.dy = dy
                    break

        # Check for wraparound at maze edges (ghosts can also use tunnels)
        # The playable maze is from y=SCORE_HEIGHT to y=SCORE_HEIGHT+maze_height
        maze_width = GRID_WIDTH * CELL_SIZE
        maze_height = GRID_HEIGHT * CELL_SIZE

        # Horizontal wraparound
        if self.rect.right < 0:  # Gone off left edge
            self.rect.x = maze_width
        elif self.rect.left > maze_width:  # Gone off right edge
            self.rect.x = -self.rect.width

        # Vertical wraparound (score area is NOT part of the playable maze)
        if self.rect.top < SCORE_HEIGHT:  # Gone into/above score area (top of screen)
            self.rect.y = maze_height + SCORE_HEIGHT - self.rect.height
        elif self.rect.top > maze_height + SCORE_HEIGHT:  # Gone off bottom edge
            self.rect.y = SCORE_HEIGHT

    def reset(self):
        """Reset ghost to starting position"""
        self.rect.x = self.start_x
        self.rect.y = self.start_y + SCORE_HEIGHT
        self.dx = random.choice([-1, 1])
        self.dy = 0
        self.image = self.create_ghost_image(self.original_color)
        self.color = self.original_color
        self.color_timer = 0
        self.color_index = 0


class Game:
    """Main game class"""

    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Pac-Man")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.large_font = pygame.font.Font(None, 72)
        self.score = 0
        self.running = True
        self.power_up_timer = 0
        self.is_powered_up = False
        self.game_state = STATE_PLAYING

        # Sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.walls = pygame.sprite.Group()
        self.pellets = pygame.sprite.Group()
        self.power_pellets = pygame.sprite.Group()
        self.ghosts = pygame.sprite.Group()

        # Load sounds
        self.load_sounds()

        self.setup_maze()

        # Start background music
        self.play_background_music()

    def load_sounds(self):
        """Load all sound effects and music"""
        # Get the directory where this script is located
        script_dir = os.path.dirname(os.path.abspath(__file__))
        sounds_dir = os.path.join(script_dir, "sounds")

        try:
            # Load background music
            music_path = os.path.join(sounds_dir, "music.mp3")
            pygame.mixer.music.load(music_path)

            # Load sound effects
            eat_pill_path = os.path.join(sounds_dir, "eatpill.mp3")
            dead_path = os.path.join(sounds_dir, "dead.mp3")

            self.eat_pill_sound = pygame.mixer.Sound(eat_pill_path)
            self.dead_sound = pygame.mixer.Sound(dead_path)

            # Set volume levels
            self.eat_pill_sound.set_volume(0.5)
            self.dead_sound.set_volume(0.7)
            pygame.mixer.music.set_volume(0.3)

        except Exception as e:
            print(f"Warning: Could not load sounds: {e}")
            # Create dummy sound objects that do nothing
            self.eat_pill_sound = None
            self.dead_sound = None

    def play_background_music(self):
        """Start playing background music in a loop"""
        try:
            pygame.mixer.music.play(-1)  # -1 means loop indefinitely
        except Exception as e:
            print(f"Warning: Could not play background music: {e}")

    def stop_background_music(self):
        """Stop the background music"""
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def setup_maze(self):
        """Parse the maze string and create sprite objects"""
        lines = [line for line in MAZE.split("\n") if line.strip()]

        ghost_colors = [RED, PINK, CYAN, ORANGE]
        ghost_index = 0

        for row, line in enumerate(lines):
            for col, char in enumerate(line):
                x = col * CELL_SIZE
                y = row * CELL_SIZE

                if char == "X":
                    wall = Wall(x, y)
                    self.walls.add(wall)
                    self.all_sprites.add(wall)
                elif char == ".":
                    pellet = Pellet(x, y)
                    self.pellets.add(pellet)
                    self.all_sprites.add(pellet)
                elif char == "S":
                    self.pacman = Pacman(x, y)
                    self.all_sprites.add(self.pacman)
                elif char == "G":
                    ghost = Ghost(x, y, ghost_colors[ghost_index % len(ghost_colors)])
                    ghost_index += 1
                    self.ghosts.add(ghost)
                    self.all_sprites.add(ghost)
                elif char == "P":
                    power_pellet = PowerPellet(x, y)
                    self.power_pellets.add(power_pellet)
                    self.all_sprites.add(power_pellet)

    def reset(self):
        """Reset the game to initial state"""
        self.score = 0
        self.power_up_timer = 0
        self.is_powered_up = False
        self.game_state = STATE_PLAYING

        # Clear all sprite groups
        self.all_sprites.empty()
        self.walls.empty()
        self.pellets.empty()
        self.power_pellets.empty()
        self.ghosts.empty()

        # Recreate the maze
        self.setup_maze()

        # Restart background music
        self.play_background_music()

    def check_circular_collision(self, sprite1, sprite2):
        """
        Check if two circular sprites are colliding using their radii.
        Returns True if distance between centers is less than sum of radii.
        """
        # Get center positions
        center1_x = sprite1.rect.centerx
        center1_y = sprite1.rect.centery
        center2_x = sprite2.rect.centerx
        center2_y = sprite2.rect.centery

        # Calculate distance between centers
        distance = ((center1_x - center2_x) ** 2 + (center1_y - center2_y) ** 2) ** 0.5

        # Get radii (approximate as half of the smaller dimension)
        radius1 = min(sprite1.rect.width, sprite1.rect.height) / 2
        radius2 = min(sprite2.rect.width, sprite2.rect.height) / 2

        # Collision occurs if distance is less than sum of radii
        return distance < (radius1 + radius2)

    def handle_events(self):
        """Handle keyboard input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.game_state == STATE_PLAYING:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_UP:
                        self.pacman.set_direction(0, -1)
                    elif event.key == pygame.K_DOWN:
                        self.pacman.set_direction(0, 1)
                    elif event.key == pygame.K_LEFT:
                        self.pacman.set_direction(-1, 0)
                    elif event.key == pygame.K_RIGHT:
                        self.pacman.set_direction(1, 0)
                elif self.game_state in (STATE_GAME_OVER, STATE_WON):
                    # In game over or won state
                    if event.key == pygame.K_r:
                        self.reset()
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False

    def update(self):
        """Update all game objects"""
        # Only update if playing
        if self.game_state != STATE_PLAYING:
            return

        # Get time delta (frame-rate independent)
        dt = self.clock.get_time() / 1000.0  # Convert to seconds
        # Clamp dt to prevent physics issues during lag spikes
        dt = min(dt, 0.05)  # Max 50ms (20 FPS minimum)

        # Update power-up timer
        if self.is_powered_up:
            self.power_up_timer -= dt
            if self.power_up_timer <= 0:
                self.is_powered_up = False
                self.power_up_timer = 0

        # Update Pacman
        self.pacman.update(self.walls, dt)

        # Update ghosts
        for ghost in self.ghosts:
            ghost.update(self.walls, self.pacman, self.is_powered_up, dt)

        # Check collision with pellets
        pellet_hits = pygame.sprite.spritecollide(self.pacman, self.pellets, True)
        for pellet in pellet_hits:
            self.score += pellet.points
            self.all_sprites.remove(pellet)
            # Play eat pill sound
            if self.eat_pill_sound:
                self.eat_pill_sound.play()

        # Check collision with power pellets
        power_pellet_hits = pygame.sprite.spritecollide(
            self.pacman, self.power_pellets, True
        )
        for pellet in power_pellet_hits:
            self.score += pellet.points
            self.all_sprites.remove(pellet)
            # Play eat pill sound
            if self.eat_pill_sound:
                self.eat_pill_sound.play()
            # Activate power-up
            self.is_powered_up = True
            self.power_up_timer = POWER_UP_DURATION

        # Check collision with ghosts (two-step collision detection)
        # Step 1: Fast bounding box collision
        ghost_hits = pygame.sprite.spritecollide(self.pacman, self.ghosts, False)

        # Step 2: Accurate circular collision detection for potential hits
        actual_collisions = []
        for ghost in ghost_hits:
            if self.check_circular_collision(self.pacman, ghost):
                actual_collisions.append(ghost)

        if actual_collisions:
            if self.is_powered_up:
                # Eat the ghosts
                for ghost in actual_collisions:
                    self.score += 200  # Bonus points for eating ghost
                    self.ghosts.remove(ghost)
                    self.all_sprites.remove(ghost)
            else:
                # Die
                self.game_state = STATE_GAME_OVER
                # Stop background music and play death sound
                self.stop_background_music()
                if self.dead_sound:
                    self.dead_sound.play()

        # Check win condition
        if len(self.pellets) == 0 and len(self.power_pellets) == 0:
            self.game_state = STATE_WON
            # Stop background music
            self.stop_background_music()

    def draw(self):
        """Draw all game objects"""
        self.screen.fill(BLACK)

        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 5))

        # Draw power-up timer if active
        if self.is_powered_up and self.game_state == STATE_PLAYING:
            timer_text = self.font.render(
                f"POWER UP: {self.power_up_timer:.1f}s", True, YELLOW
            )
            self.screen.blit(timer_text, (SCREEN_WIDTH - 250, 5))

        # Draw all sprites
        self.all_sprites.draw(self.screen)

        # Draw game over or win message
        if self.game_state == STATE_GAME_OVER:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            # Game over text
            game_over_text = self.large_font.render("GAME OVER!", True, RED)
            game_over_rect = game_over_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            )
            self.screen.blit(game_over_text, game_over_rect)

            # Instructions
            restart_text = self.font.render("Press R to Restart", True, WHITE)
            restart_rect = restart_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20)
            )
            self.screen.blit(restart_text, restart_rect)

            quit_text = self.font.render("Press ESC to Quit", True, WHITE)
            quit_rect = quit_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60)
            )
            self.screen.blit(quit_text, quit_rect)

        elif self.game_state == STATE_WON:
            # Semi-transparent overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            self.screen.blit(overlay, (0, 0))

            # Win text
            win_text = self.large_font.render("YOU WIN!", True, GREEN)
            win_rect = win_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50)
            )
            self.screen.blit(win_text, win_rect)

            # Final score
            final_score_text = self.font.render(
                f"Final Score: {self.score}", True, YELLOW
            )
            final_score_rect = final_score_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
            )
            self.screen.blit(final_score_text, final_score_rect)

            # Instructions
            restart_text = self.font.render("Press R to Restart", True, WHITE)
            restart_rect = restart_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
            )
            self.screen.blit(restart_text, restart_rect)

            quit_text = self.font.render("Press ESC to Quit", True, WHITE)
            quit_rect = quit_text.get_rect(
                center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 90)
            )
            self.screen.blit(quit_text, quit_rect)

        pygame.display.flip()

    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game"""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
