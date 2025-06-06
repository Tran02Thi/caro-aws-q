import pygame
import sys

# Khởi tạo pygame
pygame.init()

# Cấu hình màn hình
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 10
CELL_SIZE = WIDTH // GRID_SIZE
LINE_WIDTH = 2
CIRCLE_WIDTH = 5
CROSS_WIDTH = 5

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Tạo màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Cờ Caro 10x10')

# Khởi tạo bảng
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
turn = 'X'  # X đi trước
game_over = False
winner = None

def draw_grid():
    # Vẽ các đường ngang
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), LINE_WIDTH)
    
    # Vẽ các đường dọc
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), LINE_WIDTH)

def draw_markers():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 'X':
                # Vẽ X
                pygame.draw.line(screen, RED, 
                                (col * CELL_SIZE + 15, row * CELL_SIZE + 15), 
                                ((col + 1) * CELL_SIZE - 15, (row + 1) * CELL_SIZE - 15), 
                                CROSS_WIDTH)
                pygame.draw.line(screen, RED, 
                                ((col + 1) * CELL_SIZE - 15, row * CELL_SIZE + 15), 
                                (col * CELL_SIZE + 15, (row + 1) * CELL_SIZE - 15), 
                                CROSS_WIDTH)
            elif board[row][col] == 'O':
                # Vẽ O
                pygame.draw.circle(screen, BLUE, 
                                  (col * CELL_SIZE + CELL_SIZE // 2, row * CELL_SIZE + CELL_SIZE // 2), 
                                  CELL_SIZE // 2 - 15, 
                                  CIRCLE_WIDTH)

def check_win(row, col):
    player = board[row][col]
    
    # Kiểm tra hàng ngang
    def check_horizontal():
        count = 0
        for c in range(GRID_SIZE):
            if board[row][c] == player:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0
        return False
    
    # Kiểm tra hàng dọc
    def check_vertical():
        count = 0
        for r in range(GRID_SIZE):
            if board[r][col] == player:
                count += 1
                if count == 5:
                    return True
            else:
                count = 0
        return False
    
    # Kiểm tra đường chéo chính
    def check_diagonal1():
        for i in range(-4, 5):
            count = 0
            for j in range(5):
                r = row + i + j
                c = col + i + j
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c] == player:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False
    
    # Kiểm tra đường chéo phụ
    def check_diagonal2():
        for i in range(-4, 5):
            count = 0
            for j in range(5):
                r = row + i + j
                c = col - i - j
                if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE and board[r][c] == player:
                    count += 1
                    if count == 5:
                        return True
                else:
                    count = 0
        return False
    
    return check_horizontal() or check_vertical() or check_diagonal1() or check_diagonal2()

def check_draw():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] is None:
                return False
    return True

def draw_game_over():
    font = pygame.font.SysFont(None, 40)
    if winner:
        text = font.render(f"Người chơi {winner} thắng!", True, BLACK)
    else:
        text = font.render("Hòa!", True, BLACK)
    
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    # Vẽ hộp thông báo
    pygame.draw.rect(screen, WHITE, (text_rect.x - 10, text_rect.y - 10, 
                                     text_rect.width + 20, text_rect.height + 20))
    pygame.draw.rect(screen, BLACK, (text_rect.x - 10, text_rect.y - 10, 
                                     text_rect.width + 20, text_rect.height + 20), 2)
    screen.blit(text, text_rect)
    
    # Vẽ nút chơi lại
    restart_font = pygame.font.SysFont(None, 30)
    restart_text = restart_font.render("Nhấn R để chơi lại", True, BLACK)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
    screen.blit(restart_text, restart_rect)

def reset_game():
    global board, turn, game_over, winner
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    turn = 'X'
    game_over = False
    winner = None

# Vòng lặp chính
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_over:
                reset_game()
        
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            mouseX, mouseY = pygame.mouse.get_pos()
            col = mouseX // CELL_SIZE
            row = mouseY // CELL_SIZE
            
            if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and board[row][col] is None:
                board[row][col] = turn
                
                if check_win(row, col):
                    game_over = True
                    winner = turn
                elif check_draw():
                    game_over = True
                
                # Đổi lượt
                turn = 'O' if turn == 'X' else 'X'
    
    # Vẽ màn hình
    screen.fill(WHITE)
    draw_grid()
    draw_markers()
    
    if game_over:
        draw_game_over()
    
    pygame.display.update()
