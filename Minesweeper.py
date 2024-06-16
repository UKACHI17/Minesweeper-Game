import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 400
screen_height = 400

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (192, 192, 192)
dark_gray = (169, 169, 169)
red = (255, 0, 0)

# Setup the screen
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minesweeper')

# Grid settings
cell_size = 20
cols = screen_width // cell_size
rows = screen_height // cell_size
mines_count = 40

# Create a 2D array for the grid
grid = [[0 for _ in range(cols)] for _ in range(rows)]
mines = set()

# Font for numbers
font = pygame.font.Font(None, 36)

def place_mines():
    while len(mines) < mines_count:
        x = random.randint(0, cols - 1)
        y = random.randint(0, rows - 1)
        if (x, y) not in mines:
            mines.add((x, y))
            grid[y][x] = -1

def calculate_numbers():
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == -1:
                continue
            count = 0
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    ny, nx = y + dy, x + dx
                    if 0 <= nx < cols and 0 <= ny < rows and grid[ny][nx] == -1:
                        count += 1
            grid[y][x] = count

def draw_grid():
    for y in range(rows):
        for x in range(cols):
            rect = pygame.Rect(x * cell_size, y * cell_size, cell_size, cell_size)
            pygame.draw.rect(screen, gray if revealed[y][x] else dark_gray, rect)
            pygame.draw.rect(screen, black, rect, 1)
            if revealed[y][x]:
                if grid[y][x] == -1:
                    pygame.draw.circle(screen, red, rect.center, cell_size // 4)
                elif grid[y][x] > 0:
                    text = font.render(str(grid[y][x]), True, black)
                    screen.blit(text, text.get_rect(center=rect.center))

def reveal_empty_cells(x, y):
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        for dy in range(-1, 2):
            for dx in range(-1, 2):
                nx, ny = cx + dx, cy + dy
                if 0 <= nx < cols and 0 <= ny < rows and not revealed[ny][nx]:
                    revealed[ny][nx] = True
                    if grid[ny][nx] == 0:
                        stack.append((nx, ny))

place_mines()
calculate_numbers()
revealed = [[False for _ in range(cols)] for _ in range(rows)]
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            x //= cell_size
            y //= cell_size
            if event.button == 1:
                if grid[y][x] == -1:
                    game_over = True
                    revealed = [[True for _ in range(cols)] for _ in range(rows)]
                else:
                    revealed[y][x] = True
                    if grid[y][x] == 0:
                        reveal_empty_cells(x, y)
            elif event.button == 3:
                # Right-click to place a flag (toggle)
                pass  # Add flagging logic here

    screen.fill(white)
    draw_grid()
    pygame.display.flip()
    pygame.time.Clock().tick(30)