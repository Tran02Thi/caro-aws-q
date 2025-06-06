import pygame
import sys
import random

# Khởi tạo pygame
pygame.init()

# Cấu hình màn hình
BOARD_SIZE = 600
BUTTON_HEIGHT = 60
BOARD_PADDING = 10  # Padding xung quanh bàn cờ
WIDTH, HEIGHT = BOARD_SIZE + 2 * BOARD_PADDING, BOARD_SIZE + BUTTON_HEIGHT + 2 * BOARD_PADDING
GRID_SIZE = 10
CELL_SIZE = BOARD_SIZE // GRID_SIZE
LINE_WIDTH = 2
CIRCLE_WIDTH = 5
CROSS_WIDTH = 5

# Vị trí bàn cờ (dịch xuống để có chỗ cho nút và thêm padding)
BOARD_OFFSET_X = BOARD_PADDING
BOARD_OFFSET_Y = BUTTON_HEIGHT + BOARD_PADDING

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 20, 20)
BLUE = (20, 20, 220)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0)
LIGHT_GRAY = (240, 240, 240)
DARK_GRAY = (160, 160, 160)
SHADOW_GRAY = (100, 100, 100)
BOARD_COLOR = (50, 50, 50)     # Màu đen nhạt cho nền
GRID_COLOR = (255, 255, 255)   # Màu trắng cho lưới

# Tạo màn hình
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Tic Tac Toe 10x10')

# Trạng thái game
MENU = 0
PLAYING = 1
GAME_OVER = 2

# Khởi tạo bảng và biến game
board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
turn = 'X'  # X đi trước
game_state = MENU
winner = None
winning_line = []  # Lưu vị trí 5 ô chiến thắng
move_history = []  # Lưu lịch sử các nước đi để undo
game_mode = None  # 'ai' hoặc 'human'
ai_player = 'O'  # AI chơi O, người chơi X

# Định nghĩa các nút game
BUTTON_WIDTH = 100
BUTTON_MARGIN = 15
total_buttons_width = 3 * BUTTON_WIDTH + 2 * BUTTON_MARGIN
start_x = (WIDTH - total_buttons_width) // 2

game_buttons = {
    'new_game': {'x': start_x, 'y': 10, 'width': BUTTON_WIDTH, 'height': 40, 'text': 'New Game'},
    'undo': {'x': start_x + BUTTON_WIDTH + BUTTON_MARGIN, 'y': 10, 'width': BUTTON_WIDTH, 'height': 40, 'text': 'Undo'},
    'exit': {'x': start_x + 2 * (BUTTON_WIDTH + BUTTON_MARGIN), 'y': 10, 'width': BUTTON_WIDTH, 'height': 40, 'text': 'Exit'}
}

# Định nghĩa các nút menu
MENU_BUTTON_WIDTH = 200
MENU_BUTTON_HEIGHT = 60
menu_start_x = (WIDTH - MENU_BUTTON_WIDTH) // 2

menu_buttons = {
    'vs_ai': {'x': menu_start_x, 'y': HEIGHT//2 - 80, 'width': MENU_BUTTON_WIDTH, 'height': MENU_BUTTON_HEIGHT, 'text': 'Play vs AI'},
    'vs_human': {'x': menu_start_x, 'y': HEIGHT//2 + 20, 'width': MENU_BUTTON_WIDTH, 'height': MENU_BUTTON_HEIGHT, 'text': '2 Players'}
}

def draw_menu():
    """Vẽ menu chính"""
    screen.fill(BOARD_COLOR)
    
    # Tiêu đề
    title_font = pygame.font.SysFont('Arial', 48, bold=True)
    title_text = title_font.render('Game Caro', True, WHITE)
    title_rect = title_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 150))
    screen.blit(title_text, title_rect)

    # Vẽ các nút menu
    font = pygame.font.SysFont('Arial', 20, bold=True)
    
    for button_name, button in menu_buttons.items():
        x, y, w, h = button['x'], button['y'], button['width'], button['height']
        
        # Vẽ bóng đổ
        pygame.draw.rect(screen, (20, 20, 20), (x + 3, y + 3, w, h), border_radius=10)
        
        # Vẽ nút chính
        if button_name == 'vs_ai':
            button_color = (70, 130, 180)  # Màu xanh dương cho AI
        else:
            button_color = (34, 139, 34)   # Màu xanh lá cho 2 người
        
        pygame.draw.rect(screen, button_color, (x, y, w, h), border_radius=10)
        pygame.draw.rect(screen, WHITE, (x, y, w, h), 3, border_radius=10)
        
        # Vẽ text
        text_surface = font.render(button['text'], True, WHITE)
        text_rect = text_surface.get_rect(center=(x + w//2, y + h//2))
        screen.blit(text_surface, text_rect)

def check_menu_button_click(pos):
    """Kiểm tra click vào nút menu"""
    x, y = pos
    for button_name, button in menu_buttons.items():
        if (button['x'] <= x <= button['x'] + button['width'] and 
            button['y'] <= y <= button['y'] + button['height']):
            return button_name
    return None

def draw_game_buttons():
    """Vẽ các nút điều khiển game"""
    font = pygame.font.SysFont('Arial', 16, bold=True)
    
    for button_name, button in game_buttons.items():
        x, y, w, h = button['x'], button['y'], button['width'], button['height']
        
        # Vẽ bóng đổ
        pygame.draw.rect(screen, (20, 20, 20), (x + 2, y + 2, w, h), border_radius=5)
        
        # Vẽ nút chính
        if button_name == 'exit':
            button_color = (180, 50, 50)  # Màu đỏ cho nút Exit
        elif button_name == 'undo' and (len(move_history) == 0 or game_mode == 'ai'):
            button_color = (60, 60, 60)   # Màu xám tối khi không thể undo
        else:
            button_color = (80, 80, 80)   # Màu xám cho các nút khác
        
        pygame.draw.rect(screen, button_color, (x, y, w, h), border_radius=5)
        pygame.draw.rect(screen, WHITE, (x, y, w, h), 2, border_radius=5)
        
        # Vẽ text
        text_color = WHITE if button_name != 'undo' or (len(move_history) > 0 and game_mode != 'ai') else GRAY
        text_surface = font.render(button['text'], True, text_color)
        text_rect = text_surface.get_rect(center=(x + w//2, y + h//2))
        screen.blit(text_surface, text_rect)

def check_game_button_click(pos):
    """Kiểm tra xem có click vào nút game nào không"""
    x, y = pos
    for button_name, button in game_buttons.items():
        if (button['x'] <= x <= button['x'] + button['width'] and 
            button['y'] <= y <= button['y'] + button['height']):
            return button_name
    return None

def draw_grid():
    # Vẽ hiệu ứng 3D cho từng ô (với padding)
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = col * CELL_SIZE + BOARD_OFFSET_X
            y = row * CELL_SIZE + BOARD_OFFSET_Y
            
            if board[row][col] is None:
                # Ô chưa chọn - hiệu ứng nổi lên
                pygame.draw.rect(screen, (30, 30, 30), (x + 2, y + 2, CELL_SIZE - 2, CELL_SIZE - 2))
                pygame.draw.rect(screen, (70, 70, 70), (x, y, CELL_SIZE - 2, CELL_SIZE - 2))
                pygame.draw.rect(screen, BOARD_COLOR, (x + 1, y + 1, CELL_SIZE - 3, CELL_SIZE - 3))
            else:
                # Ô đã chọn - hiệu ứng ấn xuống
                pygame.draw.rect(screen, (30, 30, 30), (x, y, CELL_SIZE - 2, CELL_SIZE - 2))
                pygame.draw.rect(screen, (45, 45, 45), (x + 2, y + 2, CELL_SIZE - 4, CELL_SIZE - 4))
    
    # Vẽ các đường ngang màu trắng
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, 
                        (BOARD_OFFSET_X, i * CELL_SIZE + BOARD_OFFSET_Y), 
                        (BOARD_OFFSET_X + BOARD_SIZE, i * CELL_SIZE + BOARD_OFFSET_Y), 
                        LINE_WIDTH)
    
    # Vẽ các đường dọc màu trắng
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, GRID_COLOR, 
                        (i * CELL_SIZE + BOARD_OFFSET_X, BOARD_OFFSET_Y), 
                        (i * CELL_SIZE + BOARD_OFFSET_X, BOARD_OFFSET_Y + BOARD_SIZE), 
                        LINE_WIDTH)
    
    # Vẽ viền ngoài màu trắng
    pygame.draw.rect(screen, GRID_COLOR, (BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_SIZE, BOARD_SIZE), 3)

def draw_markers():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            center_x = col * CELL_SIZE + CELL_SIZE // 2 + BOARD_OFFSET_X
            center_y = row * CELL_SIZE + CELL_SIZE // 2 + BOARD_OFFSET_Y
            
            if board[row][col] == 'X':
                # Vẽ X với hiệu ứng 3D
                shadow_offset = 2
                pygame.draw.line(screen, SHADOW_GRAY, 
                                (col * CELL_SIZE + 12 + shadow_offset + BOARD_OFFSET_X, row * CELL_SIZE + 12 + shadow_offset + BOARD_OFFSET_Y), 
                                ((col + 1) * CELL_SIZE - 12 + shadow_offset + BOARD_OFFSET_X, (row + 1) * CELL_SIZE - 12 + shadow_offset + BOARD_OFFSET_Y), 
                                CROSS_WIDTH + 2)
                pygame.draw.line(screen, SHADOW_GRAY, 
                                ((col + 1) * CELL_SIZE - 12 + shadow_offset + BOARD_OFFSET_X, row * CELL_SIZE + 12 + shadow_offset + BOARD_OFFSET_Y), 
                                (col * CELL_SIZE + 12 + shadow_offset + BOARD_OFFSET_X, (row + 1) * CELL_SIZE - 12 + shadow_offset + BOARD_OFFSET_Y), 
                                CROSS_WIDTH + 2)
                
                pygame.draw.line(screen, (180, 0, 0), 
                                (col * CELL_SIZE + 10 + BOARD_OFFSET_X, row * CELL_SIZE + 10 + BOARD_OFFSET_Y), 
                                ((col + 1) * CELL_SIZE - 10 + BOARD_OFFSET_X, (row + 1) * CELL_SIZE - 10 + BOARD_OFFSET_Y), 
                                CROSS_WIDTH + 4)
                pygame.draw.line(screen, RED, 
                                (col * CELL_SIZE + 12 + BOARD_OFFSET_X, row * CELL_SIZE + 12 + BOARD_OFFSET_Y), 
                                ((col + 1) * CELL_SIZE - 12 + BOARD_OFFSET_X, (row + 1) * CELL_SIZE - 12 + BOARD_OFFSET_Y), 
                                CROSS_WIDTH)
                
                pygame.draw.line(screen, (180, 0, 0), 
                                ((col + 1) * CELL_SIZE - 10 + BOARD_OFFSET_X, row * CELL_SIZE + 10 + BOARD_OFFSET_Y), 
                                (col * CELL_SIZE + 10 + BOARD_OFFSET_X, (row + 1) * CELL_SIZE - 10 + BOARD_OFFSET_Y), 
                                CROSS_WIDTH + 4)
                pygame.draw.line(screen, RED, 
                                ((col + 1) * CELL_SIZE - 12 + BOARD_OFFSET_X, row * CELL_SIZE + 12 + BOARD_OFFSET_Y), 
                                (col * CELL_SIZE + 12 + BOARD_OFFSET_X, (row + 1) * CELL_SIZE - 12 + BOARD_OFFSET_Y), 
                                CROSS_WIDTH)
                
            elif board[row][col] == 'O':
                # Vẽ O với hiệu ứng 3D
                radius = CELL_SIZE // 2 - 12
                
                shadow_offset = 2
                pygame.draw.circle(screen, SHADOW_GRAY, 
                                  (center_x + shadow_offset, center_y + shadow_offset), 
                                  radius + 2, 
                                  CIRCLE_WIDTH + 2)
                
                pygame.draw.circle(screen, (0, 0, 180), 
                                  (center_x, center_y), 
                                  radius + 2, 
                                  CIRCLE_WIDTH + 4)
                
                pygame.draw.circle(screen, BLUE, 
                                  (center_x, center_y), 
                                  radius, 
                                  CIRCLE_WIDTH)
                
                highlight_x = center_x - radius // 3
                highlight_y = center_y - radius // 3
                pygame.draw.circle(screen, (100, 100, 255), 
                                  (highlight_x, highlight_y), 
                                  radius // 4, 
                                  2)

def draw_winning_line():
    """Vẽ đường thắng lên 5 ô chiến thắng - nhỏ gọn màu trắng"""
    if winning_line and len(winning_line) >= 2:
        start_row, start_col = winning_line[0]
        end_row, end_col = winning_line[-1]
        
        start_x = start_col * CELL_SIZE + CELL_SIZE // 2 + BOARD_OFFSET_X
        start_y = start_row * CELL_SIZE + CELL_SIZE // 2 + BOARD_OFFSET_Y
        end_x = end_col * CELL_SIZE + CELL_SIZE // 2 + BOARD_OFFSET_X
        end_y = end_row * CELL_SIZE + CELL_SIZE // 2 + BOARD_OFFSET_Y
        
        pygame.draw.line(screen, WHITE, (start_x, start_y), (end_x, end_y), 4)

def check_win(row, col):
    """Kiểm tra thắng và trả về vị trí các ô thắng"""
    global winning_line
    player = board[row][col]
    
    def check_horizontal():
        positions = []
        count = 0
        for c in range(GRID_SIZE):
            if board[row][c] == player:
                positions.append((row, c))
                count += 1
                if count == 5:
                    return positions[-5:]
            else:
                positions = []
                count = 0
        return None
    
    def check_vertical():
        positions = []
        count = 0
        for r in range(GRID_SIZE):
            if board[r][col] == player:
                positions.append((r, col))
                count += 1
                if count == 5:
                    return positions[-5:]
            else:
                positions = []
                count = 0
        return None
    
    def check_diagonal1():
        start_row = row
        start_col = col
        while start_row > 0 and start_col > 0:
            start_row -= 1
            start_col -= 1
        
        positions = []
        count = 0
        r, c = start_row, start_col
        while r < GRID_SIZE and c < GRID_SIZE:
            if board[r][c] == player:
                positions.append((r, c))
                count += 1
                if count == 5:
                    return positions[-5:]
            else:
                positions = []
                count = 0
            r += 1
            c += 1
        return None
    
    def check_diagonal2():
        start_row = row
        start_col = col
        while start_row > 0 and start_col < GRID_SIZE - 1:
            start_row -= 1
            start_col += 1
        
        positions = []
        count = 0
        r, c = start_row, start_col
        while r < GRID_SIZE and c >= 0:
            if board[r][c] == player:
                positions.append((r, c))
                count += 1
                if count == 5:
                    return positions[-5:]
            else:
                positions = []
                count = 0
            r += 1
            c -= 1
        return None
    
    result = check_horizontal() or check_vertical() or check_diagonal1() or check_diagonal2()
    if result:
        winning_line = result
        return True
    return False

def check_draw():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] is None:
                return False
    return True

def evaluate_position(player):
    """Đánh giá vị trí hiện tại cho AI"""
    score = 0
    opponent = 'X' if player == 'O' else 'O'
    
    # Kiểm tra tất cả các hướng có thể
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            for dr, dc in directions:
                # Đếm quân liên tiếp của player
                player_count = 0
                opponent_count = 0
                empty_count = 0
                
                for i in range(5):
                    r, c = row + i * dr, col + i * dc
                    if 0 <= r < GRID_SIZE and 0 <= c < GRID_SIZE:
                        if board[r][c] == player:
                            player_count += 1
                        elif board[r][c] == opponent:
                            opponent_count += 1
                        else:
                            empty_count += 1
                    else:
                        break
                
                # Tính điểm dựa trên số quân liên tiếp
                if opponent_count == 0:  # Không bị chặn bởi đối thủ
                    if player_count == 4:
                        score += 10000  # Sắp thắng
                    elif player_count == 3:
                        score += 1000
                    elif player_count == 2:
                        score += 100
                    elif player_count == 1:
                        score += 10
                
                # Chặn đối thủ
                if player_count == 0:
                    if opponent_count == 4:
                        score += 5000  # Chặn đối thủ sắp thắng
                    elif opponent_count == 3:
                        score += 500
                    elif opponent_count == 2:
                        score += 50
    
    return score

def get_ai_move():
    """AI chọn nước đi tốt nhất"""
    best_score = -float('inf')
    best_moves = []
    
    # Thử tất cả các ô trống
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] is None:
                # Thử đặt quân AI
                board[row][col] = ai_player
                score = evaluate_position(ai_player)
                board[row][col] = None
                
                if score > best_score:
                    best_score = score
                    best_moves = [(row, col)]
                elif score == best_score:
                    best_moves.append((row, col))
    
    # Chọn ngẫu nhiên từ các nước đi tốt nhất
    if best_moves:
        return random.choice(best_moves)
    
    # Fallback: chọn ô trống đầu tiên
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] is None:
                return (row, col)
    
    return None

def draw_game_over():
    overlay = pygame.Surface((WIDTH, HEIGHT))
    overlay.set_alpha(128)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))
    
    font = pygame.font.SysFont('Arial', 40, bold=True)
    if winner:
        if game_mode == 'ai' and winner == ai_player:
            text = font.render("AI Wins!", True, BLACK)
        elif game_mode == 'ai' and winner != ai_player:
            text = font.render("You Win!", True, BLACK)
        else:
            text = font.render(f"Player {winner} Wins!", True, BLACK)
    else:
        text = font.render("Draw!", True, BLACK)
    
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    
    box_rect = (text_rect.x - 20, text_rect.y - 20, text_rect.width + 40, text_rect.height + 60)
    
    shadow_rect = (box_rect[0] + 5, box_rect[1] + 5, box_rect[2], box_rect[3])
    pygame.draw.rect(screen, SHADOW_GRAY, shadow_rect, border_radius=10)
    
    pygame.draw.rect(screen, LIGHT_GRAY, box_rect, border_radius=10)
    pygame.draw.rect(screen, DARK_GRAY, box_rect, 3, border_radius=10)
    
    screen.blit(text, text_rect)
    
    restart_font = pygame.font.SysFont('Arial', 24)
    restart_text = restart_font.render("Press R to restart", True, BLACK)
    restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    
    button_rect = (restart_rect.x - 10, restart_rect.y - 5, restart_rect.width + 20, restart_rect.height + 10)
    pygame.draw.rect(screen, WHITE, button_rect, border_radius=5)
    pygame.draw.rect(screen, GRAY, button_rect, 2, border_radius=5)
    
    screen.blit(restart_text, restart_rect)

def reset_game():
    global board, turn, game_state, winner, winning_line, move_history
    board = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    turn = 'X'
    game_state = PLAYING
    winner = None
    winning_line = []
    move_history = []

def undo_move():
    global turn, winner, winning_line
    if len(move_history) > 0 and game_mode == 'human':
        last_move = move_history.pop()
        row, col = last_move
        board[row][col] = None
        turn = 'O' if turn == 'X' else 'X'
        winning_line = []

def make_move(row, col):
    """Thực hiện nước đi"""
    global turn, game_state, winner
    
    board[row][col] = turn
    move_history.append((row, col))
    
    if check_win(row, col):
        game_state = GAME_OVER
        winner = turn
    elif check_draw():
        game_state = GAME_OVER
        winner = None
    else:
        # Đổi lượt
        turn = 'O' if turn == 'X' else 'X'

# Vòng lặp chính
clock = pygame.time.Clock()
ai_move_timer = 0

while True:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and game_state == GAME_OVER:
                reset_game()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouseX, mouseY = pygame.mouse.get_pos()
            
            if game_state == MENU:
                # Xử lý click menu
                button_clicked = check_menu_button_click((mouseX, mouseY))
                if button_clicked == 'vs_ai':
                    game_mode = 'ai'
                    reset_game()
                elif button_clicked == 'vs_human':
                    game_mode = 'human'
                    reset_game()
            
            elif game_state == PLAYING:
                # Kiểm tra click vào nút game
                button_clicked = check_game_button_click((mouseX, mouseY))
                if button_clicked:
                    if button_clicked == 'new_game':
                        game_state = MENU
                    elif button_clicked == 'undo':
                        undo_move()
                    elif button_clicked == 'exit':
                        game_state = MENU
                
                # Kiểm tra click vào bàn cờ
                elif mouseY >= BOARD_OFFSET_Y and mouseX >= BOARD_OFFSET_X:
                    if game_mode == 'human' or (game_mode == 'ai' and turn == 'X'):
                        col = (mouseX - BOARD_OFFSET_X) // CELL_SIZE
                        row = (mouseY - BOARD_OFFSET_Y) // CELL_SIZE
                        
                        if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and board[row][col] is None:
                            make_move(row, col)
            
            elif game_state == GAME_OVER:
                # Kiểm tra click vào nút game
                button_clicked = check_game_button_click((mouseX, mouseY))
                if button_clicked:
                    if button_clicked == 'new_game' or button_clicked == 'exit':
                        game_state = MENU
    
    # AI move
    if (game_state == PLAYING and game_mode == 'ai' and turn == ai_player):
        ai_move_timer += dt
        if ai_move_timer > 500:  # Delay 500ms cho AI
            ai_move = get_ai_move()
            if ai_move:
                row, col = ai_move
                make_move(row, col)
            ai_move_timer = 0
    else:
        ai_move_timer = 0
    
    # Vẽ màn hình
    if game_state == MENU:
        draw_menu()
    else:
        screen.fill(BOARD_COLOR)
        draw_game_buttons()
        draw_grid()
        draw_markers()
        
        if game_state == GAME_OVER and winner:
            draw_winning_line()
        
        if game_state == GAME_OVER:
            draw_game_over()
    
    pygame.display.update()
