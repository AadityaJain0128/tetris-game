"""
Tetris Game - A complete implementation with modern features
Features: Ghost piece, hold piece, next piece preview, scoring, levels
"""

import random
from typing import List, Optional, Tuple

import pygame

# Initialize Pygame
pygame.init()


class GameConfig:  # pylint: disable=too-few-public-methods
    """
    Central configuration for screen, grid, gameplay timings and colors.
    Attributes:
    SCREEN_WIDTH: Width of window in pixels.
    SCREEN_HEIGHT: Height of window in pixels.
    BLOCK_SIZE: Pixel size of each grid cell.
    GRID_X: X offset for drawing grid.
    GRID_Y: Y offset for drawing grid.
    GRID_WIDTH: Width of the Tetris grid in cells.
    GRID_HEIGHT: Height of the Tetris grid in cells.
    INITIAL_FALL_SPEED: Milliseconds between automatic piece drops.
    CLEAR_ANIMATION_DURATION: Duration of line clear fade animation.
    LEVEL_SPEED_DECREASE: Speed increase per level.
    MIN_FALL_SPEED: Minimum allowed fall speed.
    LINE_SCORES: Points awarded for clearing 1–4 lines.
    SOFT_DROP_BONUS: Points per cell when soft dropping.
    HARD_DROP_BONUS: Points per cell when hard dropping.
    LINES_PER_LEVEL: Lines needed to level up.
    SHAPES: Binary matrices for every Tetromino.
    COLORS: RGB colors for each Tetromino type.
    """

    # Display settings
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 700
    BLOCK_SIZE = 30
    GRID_X = 250
    GRID_Y = 50

    # Grid settings
    GRID_WIDTH = 10
    GRID_HEIGHT = 20

    # Timing settings
    INITIAL_FALL_SPEED = 1000  # milliseconds
    CLEAR_ANIMATION_DURATION = 500  # milliseconds
    LEVEL_SPEED_DECREASE = 100  # milliseconds
    MIN_FALL_SPEED = 100  # milliseconds

    # Scoring
    LINE_SCORES = {1: 100, 2: 300, 3: 500, 4: 800}
    SOFT_DROP_BONUS = 1
    HARD_DROP_BONUS = 2
    LINES_PER_LEVEL = 10

    # Colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (128, 128, 128)
    DARK_GRAY = (40, 40, 40)
    CYAN = (0, 255, 255)
    YELLOW = (255, 255, 0)
    PURPLE = (128, 0, 128)
    GREEN = (0, 255, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    ORANGE = (255, 165, 0)

    # Tetromino shapes
    SHAPES = {
        "I": [[1, 1, 1, 1]],
        "O": [[1, 1], [1, 1]],
        "T": [[0, 1, 0], [1, 1, 1]],
        "S": [[0, 1, 1], [1, 1, 0]],
        "Z": [[1, 1, 0], [0, 1, 1]],
        "J": [[1, 0, 0], [1, 1, 1]],
        "L": [[0, 0, 1], [1, 1, 1]],
    }

    # Tetromino colors (defined inline to avoid forward reference issues)
    COLORS = {
        "I": (0, 255, 255),  # CYAN
        "O": (255, 255, 0),  # YELLOW
        "T": (128, 0, 128),  # PURPLE
        "S": (0, 255, 0),  # GREEN
        "Z": (255, 0, 0),  # RED
        "J": (0, 0, 255),  # BLUE
        "L": (255, 165, 0),  # ORANGE
    }


# Module-level constants for backward compatibility
SCREEN_WIDTH = GameConfig.SCREEN_WIDTH
SCREEN_HEIGHT = GameConfig.SCREEN_HEIGHT
GRID_WIDTH = GameConfig.GRID_WIDTH
GRID_HEIGHT = GameConfig.GRID_HEIGHT
BLOCK_SIZE = GameConfig.BLOCK_SIZE
GRID_X = GameConfig.GRID_X
GRID_Y = GameConfig.GRID_Y

BLACK = GameConfig.BLACK
WHITE = GameConfig.WHITE
GRAY = GameConfig.GRAY
DARK_GRAY = GameConfig.DARK_GRAY
CYAN = GameConfig.CYAN
YELLOW = GameConfig.YELLOW
PURPLE = GameConfig.PURPLE
GREEN = GameConfig.GREEN
RED = GameConfig.RED
BLUE = GameConfig.BLUE
ORANGE = GameConfig.ORANGE

SHAPES = GameConfig.SHAPES
COLORS = GameConfig.COLORS


class GameState:
    """
    Base class for representing a game state.
    Methods are overridden by specific states.
    """

    def handle_input(self, event: pygame.event.Event, game: "TetrisGame") -> None:
        """Handle keyboard input for this state."""

    def update(self, delta_time: int, game: "TetrisGame") -> None:
        """
        Update the logic of the state.
        Args:
        delta_time: Milliseconds since last frame.
        """

    def draw(self, game: "TetrisGame") -> None:
        """Draw additional UI elements for this state if needed."""


class PlayingState(GameState):
    """State representing active gameplay."""

    def handle_input(self, event: pygame.event.Event, game: "TetrisGame") -> None:
        """
        Process input while playing.
        Supports movement, rotation, drops, hold piece, pause and ghost toggle.
        """
        if event.key == pygame.K_LEFT:
            game.move_piece(-1, 0)
        elif event.key == pygame.K_RIGHT:
            game.move_piece(1, 0)
        elif event.key == pygame.K_DOWN:
            if game.move_piece(0, 1):
                game.score += game.config.SOFT_DROP_BONUS
        elif event.key == pygame.K_UP:
            game.rotate_piece()
        elif event.key == pygame.K_SPACE:
            game.hard_drop()
        elif event.key == pygame.K_c:
            game.hold_current_piece()
        elif event.key == pygame.K_g:
            game.show_ghost = not game.show_ghost
        elif event.key == pygame.K_p:
            game.state = PausedState()

    def update(self, delta_time: int, game: "TetrisGame") -> None:
        """Auto-drop piece and lock it if movement fails."""
        # Auto-fall
        game.fall_time += delta_time
        if game.fall_time >= game.fall_speed:
            game.fall_time = 0
            if not game.move_piece(0, 1):
                game.lock_piece()

    def draw(self, game: "TetrisGame") -> None:
        """No additional drawing needed for playing state"""


class PausedState(GameState):
    """State representing pause menu."""

    def handle_input(self, event: pygame.event.Event, game: "TetrisGame") -> None:
        """Unpause when pressing P."""
        if event.key == pygame.K_p:
            game.state = PlayingState()

    def update(self, delta_time: int, game: "TetrisGame") -> None:
        """No updates while paused"""

    def draw(self, game: "TetrisGame") -> None:
        """Draw semi-transparent pause overlay with text."""
        overlay = pygame.Surface((game.config.SCREEN_WIDTH, game.config.SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill(game.config.BLACK)
        game.screen.blit(overlay, (0, 0))

        pause_text = game.font.render("PAUSED", True, game.config.WHITE)
        continue_text = game.small_font.render("Press P to Continue", True, game.config.WHITE)

        game.screen.blit(
            pause_text,
            (game.config.SCREEN_WIDTH // 2 - pause_text.get_width() // 2, 250),
        )
        game.screen.blit(
            continue_text,
            (game.config.SCREEN_WIDTH // 2 - continue_text.get_width() // 2, 320),
        )


class LineClearingState(GameState):
    """State representing line-clearing fade animation."""

    def handle_input(self, event: pygame.event.Event, game: "TetrisGame") -> None:
        """No input handling during line clearing"""

    def update(self, delta_time: int, game: "TetrisGame") -> None:
        """Update fade animation progress and complete when time is up."""
        game.clear_animation_time += delta_time
        if game.clear_animation_time >= game.clear_animation_duration:
            game.finish_clearing_animation()
            game.state = PlayingState()

    def draw(self, game: "TetrisGame") -> None:
        """No additional drawing needed - animation handled in draw_grid"""


class GameOverState(GameState):
    """State shown after a losing position occurs."""

    def handle_input(self, event: pygame.event.Event, game: "TetrisGame") -> None:
        """Restart game when pressing R."""
        if event.key == pygame.K_r:
            game.reset_game()
            game.state = PlayingState()

    def update(self, delta_time: int, game: "TetrisGame") -> None:
        """No updates in game over state"""

    def draw(self, game: "TetrisGame") -> None:
        """Show game over overlay and final score."""
        overlay = pygame.Surface((game.config.SCREEN_WIDTH, game.config.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill(game.config.BLACK)
        game.screen.blit(overlay, (0, 0))

        game_over_text = game.font.render("GAME OVER", True, game.config.RED)
        score_text = game.font.render(f"Final Score: {game.score}", True, game.config.WHITE)
        restart_text = game.small_font.render("Press R to Restart", True, game.config.WHITE)

        game.screen.blit(
            game_over_text,
            (game.config.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 250),
        )
        game.screen.blit(
            score_text,
            (game.config.SCREEN_WIDTH // 2 - score_text.get_width() // 2, 320),
        )
        game.screen.blit(
            restart_text,
            (game.config.SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 400),
        )


class Tetromino:
    """
    Represents a falling Tetris piece and its rotation matrix.
    Attributes:
    type: String key like "I", "O", etc.
    shape: 2D list defining block cells.
    color: RGB tuple.
    x: Grid X coordinate (integer cell index).
    y: Grid Y coordinate.
    """

    def __init__(self, shape_type: str, config: Optional[type] = None) -> None:
        """
        Initialize a Tetromino.

        Args:
            shape_type: Type of tetromino ("I", "O", "T", "S", "Z", "J", "L")
            config: Configuration class (not instance) to use. Defaults to GameConfig.
                   Using a class allows for easy subclassing and attribute access.
        """
        if config is None:
            config = GameConfig
        self.type = shape_type
        self.shape = [row[:] for row in config.SHAPES[shape_type]]
        self.color = config.COLORS[shape_type]
        self.x = config.GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
        self.config = config

    def rotate_clockwise(self) -> None:
        """Rotate piece 90 degrees clockwise by matrix transpose + reverse."""
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def rotate_counterclockwise(self) -> None:
        """Rotate piece 90 degrees counterclockwise."""
        self.shape = [list(row) for row in zip(*self.shape)][::-1]

    def get_blocks(self) -> List[Tuple[int, int]]:
        """Return list of (x, y) grid coordinates occupied by this piece."""
        blocks = []
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell:
                    blocks.append((self.x + x, self.y + y))
        return blocks

    def copy(self) -> "Tetromino":
        """Create a separate copy of the piece, preserving orientation."""
        new_piece = Tetromino(self.type, self.config)
        new_piece.shape = [row[:] for row in self.shape]
        new_piece.x = self.x
        new_piece.y = self.y
        return new_piece


class TetrisGame:
    """Manages grid, active piece, input, drawing and game state transitions."""

    def __init__(self, config: Optional[type] = None) -> None:
        """
        Initialize the Tetris game.

        Args:
            config: Configuration class (not instance) to use. Defaults to GameConfig.
                   Using a class allows for easy subclassing and attribute access.
                   Example:
                       game = TetrisGame()  # Use default config
                       game = TetrisGame(CustomConfig)  # Use custom config class
        """
        if config is None:
            config = GameConfig
        self.config = config

        self.screen = pygame.display.set_mode((self.config.SCREEN_WIDTH, self.config.SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris - Ultimate Edition")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)

        # Game state
        self.grid = [
            [None for _ in range(self.config.GRID_WIDTH)] for _ in range(self.config.GRID_HEIGHT)
        ]
        self.current_piece: Optional[Tetromino] = None
        self.next_piece: Optional[Tetromino] = None
        self.hold_piece: Optional[Tetromino] = None
        self.can_hold = True
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False

        # Timing
        self.fall_time = 0
        self.fall_speed = self.config.INITIAL_FALL_SPEED

        # Animation state
        self.clearing_lines = []
        self.clear_animation_time = 0
        self.clear_animation_duration = self.config.CLEAR_ANIMATION_DURATION

        # Settings
        self.show_ghost = True

        # State pattern
        self.state: GameState = PlayingState()

        # Initialize first pieces
        self.next_piece = self.get_random_piece()
        self.spawn_new_piece()

    def get_random_piece(self) -> Tetromino:
        """Return a random Tetromino instance."""
        return Tetromino(random.choice(list(self.config.SHAPES.keys())), self.config)

    def spawn_new_piece(self) -> None:
        """
        Move next piece into play and create a new next piece.
        Handles game over if spawn location is blocked.
        """
        self.current_piece = self.next_piece
        self.next_piece = self.get_random_piece()
        self.can_hold = True

        # Check if game over
        if not self.is_valid_position(self.current_piece):
            self.game_over = True
            self.state = GameOverState()

    def is_valid_position(self, piece: Tetromino, offset_x: int = 0, offset_y: int = 0) -> bool:
        """
        Check if piece can occupy position with given offset.
        Args:
        piece: Tetromino to test.
        offset_x: Horizontal offset from current x.
        offset_y: Vertical offset.
        Returns:
        True if all blocks are inside bounds and not colliding.
        """
        for x, y in piece.get_blocks():
            new_x = x + offset_x
            new_y = y + offset_y

            # Check boundaries
            if new_x < 0 or new_x >= self.config.GRID_WIDTH or new_y >= self.config.GRID_HEIGHT:
                return False

            # Check collision with placed blocks
            if new_y >= 0 and self.grid[new_y][new_x] is not None:
                return False

        return True

    def move_piece(self, dx: int, dy: int) -> bool:
        """
        Attempt to move the active piece.
        Args:
        dx: Horizontal movement.
        dy: Vertical movement.
        Returns:
        True if movement succeeded, False otherwise.
        """
        if self.is_valid_position(self.current_piece, dx, dy):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False

    def rotate_piece(self) -> None:
        """Attempt rotation with simple wall kicks."""
        original_shape = [row[:] for row in self.current_piece.shape]
        self.current_piece.rotate_clockwise()

        # Try wall kicks
        kicks = [(0, 0), (-1, 0), (1, 0), (0, -1), (-1, -1), (1, -1)]
        for dx, dy in kicks:
            if self.is_valid_position(self.current_piece, dx, dy):
                self.current_piece.x += dx
                self.current_piece.y += dy
                return

        # Rotation failed, restore original shape
        self.current_piece.shape = original_shape

    def hard_drop(self) -> None:
        """Drop piece instantly to floor, awarding bonus points."""
        drop_distance = 0
        while self.move_piece(0, 1):
            drop_distance += 1

        self.score += drop_distance * self.config.HARD_DROP_BONUS
        self.lock_piece()

    def get_ghost_piece(self) -> Tetromino:
        """Return ghost copy showing landing position of current piece."""
        ghost = self.current_piece.copy()
        while self.is_valid_position(ghost, 0, 1):
            ghost.y += 1
        return ghost

    def lock_piece(self) -> None:
        """Place piece permanently into grid and check for line clears."""
        for x, y in self.current_piece.get_blocks():
            if y >= 0:
                self.grid[y][x] = self.current_piece.color

        self.clear_lines()
        if not self.clearing_lines:
            self.spawn_new_piece()

    def clear_lines(self) -> None:
        """
        Identify filled lines, start animation and update score and level.
        Side effects:
        Sets clearing_lines.
        Updates score and level.
        Switches state to LineClearingState if necessary.
        """
        lines_to_clear = []

        for y in range(self.config.GRID_HEIGHT):
            if all(self.grid[y][x] is not None for x in range(self.config.GRID_WIDTH)):
                lines_to_clear.append(y)

        if lines_to_clear:
            # Start animation
            self.clearing_lines = lines_to_clear[:]
            self.clear_animation_time = 0

            # Update score and level
            num_lines = len(lines_to_clear)
            self.lines_cleared += num_lines

            # Scoring using config
            self.score += self.config.LINE_SCORES.get(num_lines, 0) * self.level

            # Level up every LINES_PER_LEVEL lines
            new_level = self.lines_cleared // self.config.LINES_PER_LEVEL + 1
            if new_level > self.level:
                self.level = new_level
                self.fall_speed = max(
                    self.config.MIN_FALL_SPEED,
                    self.config.INITIAL_FALL_SPEED
                    - (self.level - 1) * self.config.LEVEL_SPEED_DECREASE,
                )

            # Transition to line clearing state
            self.state = LineClearingState()

    def finish_clearing_animation(self) -> None:
        """Remove cleared lines and shift grid downward after animation."""
        if self.clearing_lines:
            for y in reversed(self.clearing_lines):
                del self.grid[y]
                self.grid.insert(0, [None for _ in range(self.config.GRID_WIDTH)])
            self.clearing_lines = []
            self.spawn_new_piece()

    def hold_current_piece(self) -> None:
        """Swap current piece with hold piece if allowed."""
        if not self.can_hold:
            return

        if self.hold_piece is None:
            self.hold_piece = Tetromino(self.current_piece.type, self.config)
            self.spawn_new_piece()
        else:
            # Swap current and hold piece
            temp_type = self.current_piece.type
            self.current_piece = Tetromino(self.hold_piece.type, self.config)
            self.hold_piece = Tetromino(temp_type, self.config)

        self.can_hold = False

    def draw_grid(self) -> None:
        """Render grid background, lines, ghost, active piece and blocks."""
        # Draw background
        grid_rect = pygame.Rect(
            self.config.GRID_X,
            self.config.GRID_Y,
            self.config.GRID_WIDTH * self.config.BLOCK_SIZE,
            self.config.GRID_HEIGHT * self.config.BLOCK_SIZE,
        )
        pygame.draw.rect(self.screen, self.config.DARK_GRAY, grid_rect)

        # Draw grid lines
        for x in range(self.config.GRID_WIDTH + 1):
            pygame.draw.line(
                self.screen,
                self.config.GRAY,
                (self.config.GRID_X + x * self.config.BLOCK_SIZE, self.config.GRID_Y),
                (
                    self.config.GRID_X + x * self.config.BLOCK_SIZE,
                    self.config.GRID_Y + self.config.GRID_HEIGHT * self.config.BLOCK_SIZE,
                ),
            )

        for y in range(self.config.GRID_HEIGHT + 1):
            pygame.draw.line(
                self.screen,
                self.config.GRAY,
                (self.config.GRID_X, self.config.GRID_Y + y * self.config.BLOCK_SIZE),
                (
                    self.config.GRID_X + self.config.GRID_WIDTH * self.config.BLOCK_SIZE,
                    self.config.GRID_Y + y * self.config.BLOCK_SIZE,
                ),
            )

        # Draw placed blocks
        for y in range(self.config.GRID_HEIGHT):
            for x in range(self.config.GRID_WIDTH):
                if self.grid[y][x] is not None:
                    self.draw_block(x, y, self.grid[y][x])

        # Draw clearing animation
        if self.clearing_lines:
            progress = self.clear_animation_time / self.clear_animation_duration
            alpha = int(255 * (1 - progress))

            for y in self.clearing_lines:
                for x in range(self.config.GRID_WIDTH):
                    rect = pygame.Rect(
                        self.config.GRID_X + x * self.config.BLOCK_SIZE + 1,
                        self.config.GRID_Y + y * self.config.BLOCK_SIZE + 1,
                        self.config.BLOCK_SIZE - 2,
                        self.config.BLOCK_SIZE - 2,
                    )
                    # Create a surface with alpha for fade effect
                    surf = pygame.Surface((self.config.BLOCK_SIZE - 2, self.config.BLOCK_SIZE - 2))
                    surf.set_alpha(alpha)
                    surf.fill(self.config.WHITE)
                    self.screen.blit(surf, (rect.x, rect.y))

        # Draw ghost piece
        if self.current_piece and self.show_ghost and not self.clearing_lines:
            ghost = self.get_ghost_piece()
            for x, y in ghost.get_blocks():
                if y >= 0:
                    rect = pygame.Rect(
                        self.config.GRID_X + x * self.config.BLOCK_SIZE + 2,
                        self.config.GRID_Y + y * self.config.BLOCK_SIZE + 2,
                        self.config.BLOCK_SIZE - 4,
                        self.config.BLOCK_SIZE - 4,
                    )
                    pygame.draw.rect(self.screen, self.current_piece.color, rect, 2)

        # Draw current piece
        if self.current_piece:
            for x, y in self.current_piece.get_blocks():
                if y >= 0:
                    self.draw_block(x, y, self.current_piece.color)

    def draw_block(self, x: int, y: int, color: Tuple[int, int, int]) -> None:
        """Draw one grid cell with shading effect."""
        rect = pygame.Rect(
            self.config.GRID_X + x * self.config.BLOCK_SIZE + 1,
            self.config.GRID_Y + y * self.config.BLOCK_SIZE + 1,
            self.config.BLOCK_SIZE - 2,
            self.config.BLOCK_SIZE - 2,
        )
        pygame.draw.rect(self.screen, color, rect)

        # Add highlight for 3D effect
        highlight = tuple(min(c + 40, 255) for c in color)
        pygame.draw.line(self.screen, highlight, (rect.left, rect.top), (rect.right, rect.top), 2)
        pygame.draw.line(self.screen, highlight, (rect.left, rect.top), (rect.left, rect.bottom), 2)

    def draw_piece_preview(self, piece: Optional[Tetromino], x: int, y: int, title: str) -> None:
        """Draw preview box for next or hold piece."""
        # Draw title
        title_text = self.small_font.render(title, True, self.config.WHITE)
        self.screen.blit(title_text, (x, y - 30))

        # Draw box
        box_rect = pygame.Rect(x, y, 120, 100)
        pygame.draw.rect(self.screen, self.config.DARK_GRAY, box_rect)
        pygame.draw.rect(self.screen, self.config.WHITE, box_rect, 2)

        # Draw piece centered in box
        if piece:
            offset_x = x + 60 - len(piece.shape[0]) * self.config.BLOCK_SIZE // 2
            offset_y = y + 50 - len(piece.shape) * self.config.BLOCK_SIZE // 2

            for row_idx, row in enumerate(piece.shape):
                for col_idx, cell in enumerate(row):
                    if cell:
                        rect = pygame.Rect(
                            offset_x + col_idx * self.config.BLOCK_SIZE,
                            offset_y + row_idx * self.config.BLOCK_SIZE,
                            self.config.BLOCK_SIZE - 2,
                            self.config.BLOCK_SIZE - 2,
                        )
                        pygame.draw.rect(self.screen, piece.color, rect)

    def draw_ui(self) -> None:
        """Draw score, level, lines, next and hold previews, and controls."""
        # Score
        score_text = self.font.render(f"Score: {self.score}", True, self.config.WHITE)
        self.screen.blit(score_text, (50, 100))

        # Level
        level_text = self.font.render(f"Level: {self.level}", True, self.config.WHITE)
        self.screen.blit(level_text, (50, 150))

        # Lines
        lines_text = self.font.render(f"Lines: {self.lines_cleared}", True, self.config.WHITE)
        self.screen.blit(lines_text, (50, 200))

        # Next piece
        self.draw_piece_preview(self.next_piece, 580, 100, "NEXT")

        # Hold piece
        self.draw_piece_preview(self.hold_piece, 580, 250, "HOLD")

        # Controls
        controls = [
            "Controls:",
            "Left/Right: Move",
            "Down: Soft Drop",
            "Up: Rotate",
            "SPACE: Hard Drop",
            "C: Hold",
            "P: Pause",
            "G: Toggle Ghost",
            "ESC: Quit",
        ]

        for i, control in enumerate(controls):
            control_text = self.small_font.render(control, True, self.config.WHITE)
            self.screen.blit(control_text, (50, 400 + i * 30))

    def reset_game(self) -> None:
        """Reset grid, stats and pieces to initial state."""
        self.grid = [
            [None for _ in range(self.config.GRID_WIDTH)] for _ in range(self.config.GRID_HEIGHT)
        ]
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.game_over = False
        self.fall_speed = self.config.INITIAL_FALL_SPEED
        self.clearing_lines = []
        self.clear_animation_time = 0
        self.next_piece = self.get_random_piece()
        self.hold_piece = None
        self.can_hold = True
        self.state = PlayingState()
        self.spawn_new_piece()

    def handle_input(self, event: pygame.event.Event) -> None:
        """Forward input to current state."""
        if event.type == pygame.KEYDOWN:
            self.state.handle_input(event, self)

    def update(self, delta_time: int) -> None:
        """Update game logic if game is not over."""
        if self.game_over:
            return

        self.state.update(delta_time, self)

    def draw(self) -> None:
        """Render full frame including grid and UI."""
        self.screen.fill(self.config.BLACK)
        self.draw_grid()
        self.draw_ui()

        # Delegate state-specific drawing to current state
        self.state.draw(self)

        pygame.display.flip()

    def run(self) -> None:
        """Main loop handling events, updates and drawing."""
        running = True

        while running:
            delta_time = self.clock.tick(60)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        self.handle_input(event)

            self.update(delta_time)
            self.draw()

        pygame.quit()


def main() -> None:
    """Start game instance and begin event loop."""
    game = TetrisGame()
    game.run()


if __name__ == "__main__":
    main()
