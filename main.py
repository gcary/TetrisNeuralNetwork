import pygame
import random

# Constants
GRID_WIDTH = 10
GRID_HEIGHT = 20
BLOCK_SIZE = 30
SCREEN_WIDTH = GRID_WIDTH * BLOCK_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * BLOCK_SIZE
FPS = 10

# Colors
COLORS = [
    (0, 0, 0),        # Black (background)
    (255, 85, 85),    # Red
    (100, 200, 115),  # Green
    (120, 108, 245),  # Blue
    (255, 140, 50),   # Orange
    (50, 120, 52),    # Dark Green
    (146, 202, 73),   # Light Green
    (150, 161, 218),  # Light Blue
]

# Shapes
SHAPES = [
    # S shape
    [[1, 1, 0],
     [0, 1, 1],
     [0, 0, 0]],

    # Z shape
    [[0, 1, 1],
     [1, 1, 0],
     [0, 0, 0]],

    # I shape
    [[1, 1, 1, 1],
     [0, 0, 0, 0],
     [0, 0, 0, 0],
     [0, 0, 0, 0]],

    # O shape
    [[1, 1],
     [1, 1]],

    # J shape
    [[1, 0, 0],
     [1, 1, 1],
     [0, 0, 0]],

    # L shape
    [[0, 0, 1],
     [1, 1, 1],
     [0, 0, 0]],

    # T shape
    [[0, 1, 0],
     [1, 1, 1],
     [0, 0, 0]]
]

# Tetrimino class
class Tetrimino:
    def __init__(self, shape):
        self.shape = shape
        self.color = random.randint(1, len(COLORS) - 1)
        self.x = GRID_WIDTH // 2 - len(shape[0]) // 2
        self.y = 0

    def rotate(self):
        # Rotates the shape 90 degrees clockwise
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

    def draw(self, screen):
        # Draws the Tetrimino on the screen
        for row_y, row in enumerate(self.shape):
            for col_x, value in enumerate(row):
                if value:
                    # Calculate the top-left corner of the block
                    top_left_x = (self.x + col_x) * BLOCK_SIZE
                    top_left_y = (self.y + row_y) * BLOCK_SIZE
                    rect = pygame.Rect(top_left_x, top_left_y, BLOCK_SIZE, BLOCK_SIZE)
                    pygame.draw.rect(screen, COLORS[self.color], rect)

# Game class
class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.grid = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
        self.tetrimino = Tetrimino(random.choice(SHAPES))
        self.running = True

    def draw_grid(self):
        # Draws the Tetris grid
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                color = COLORS[self.grid[y][x]]
                rect = pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def check_collision(self, dx=0, dy=0):
        # Checks for collisions with other blocks or the grid boundaries
        shape = self.tetrimino.shape
        x = self.tetrimino.x + dx
        y = self.tetrimino.y + dy

        for row_y, row in enumerate(shape):
            for col_x, value in enumerate(row):
                if value:
                    # Check if it goes out of bounds
                    if not (0 <= x + col_x < GRID_WIDTH) or y + row_y >= GRID_HEIGHT:
                        return True
                    # Check if it collides with the grid
                    if self.grid[y + row_y][x + col_x]:
                        return True
        return False

    def freeze_tetrimino(self):
        # Freezes the current Tetrimino in place on the grid
        shape = self.tetrimino.shape
        x = self.tetrimino.x
        y = self.tetrimino.y

        for row_y, row in enumerate(shape):
            for col_x, value in enumerate(row):
                if value:
                    self.grid[y + row_y][x + col_x] = self.tetrimino.color

    def clear_lines(self):
        # Clears completed lines from the grid
        lines_cleared = 0
        for y in range(GRID_HEIGHT - 1, -1, -1):
            if all(self.grid[y]):
                lines_cleared += 1
                # Remove the full line
                del self.grid[y]
                # Add an empty line at the top
                self.grid.insert(0, [0] * GRID_WIDTH)
        return lines_cleared

    def game_over(self):
        # Checks if the game is over (when blocks reach the top)
        return any(self.grid[0])

    def play(self):
        # Main game loop
        while self.running:
            self.screen.fill((0, 0, 0))

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT and not self.check_collision(dx=-1):
                        self.tetrimino.x -= 1
                    elif event.key == pygame.K_RIGHT and not self.check_collision(dx=1):
                        self.tetrimino.x += 1
                    elif event.key == pygame.K_DOWN and not self.check_collision(dy=1):
                        self.tetrimino.y += 1
                    elif event.key == pygame.K_UP:
                        # Rotate the Tetrimino
                        self.tetrimino.rotate()
                        if self.check_collision():
                            # Reverse the rotation if it causes a collision
                            self.tetrimino.rotate()
                            self.tetrimino.rotate()
                            self.tetrimino.rotate()

            # Update game state
            if not self.check_collision(dy=1):
                self.tetrimino.y += 1
            else:
                # Freeze Tetrimino and create a new one
                self.freeze_tetrimino()
                self.clear_lines()
                if self.game_over():
                    self.running = False
                else:
                    self.tetrimino = Tetrimino(random.choice(SHAPES))

            # Draw grid and Tetrimino
            self.draw_grid()
            self.tetrimino.draw(self.screen)

            # Update the display
            pygame.display.flip()

            # Control the game speed
            self.clock.tick(FPS)

        pygame.quit()

# Run the game
if __name__ == "__main__":
    game = Tetris()
    game.play()
