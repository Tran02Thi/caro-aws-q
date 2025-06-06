# Game Cờ Caro 10x10

Game cờ caro đơn giản được phát triển bằng Python và thư viện Pygame. Trò chơi cho phép hai người chơi thay phiên nhau đánh dấu X và O trên bảng 10x10, với mục tiêu tạo được 5 quân liên tiếp theo hàng ngang, dọc hoặc đường chéo.

## Yêu cầu hệ thống

- Python 3.x
- Pygame

## Cài đặt

1. Đảm bảo bạn đã cài đặt Python 3.x
2. Cài đặt thư viện Pygame bằng lệnh:
   ```
   pip install pygame
   ```
3. Tải file `caro.py` và chạy:
   ```
   python caro.py
   ```

## Cách chơi

- Người chơi X (màu đỏ) đi trước
- Click chuột để đặt quân X hoặc O vào ô trống
- Thắng khi có 5 quân liên tiếp theo hàng ngang, dọc hoặc chéo
- Khi trò chơi kết thúc, nhấn phím R để chơi lại

## Giải thích mã nguồn

### Các biến và cấu hình chính

- `WIDTH, HEIGHT`: Kích thước màn hình (600x600 pixels)
- `GRID_SIZE`: Kích thước bảng (10x10)
- `CELL_SIZE`: Kích thước mỗi ô (60x60 pixels)
- `board`: Ma trận 10x10 lưu trạng thái bảng (None, 'X', hoặc 'O')
- `turn`: Lượt chơi hiện tại ('X' hoặc 'O')
- `game_over`: Trạng thái kết thúc trò chơi
- `winner`: Người thắng cuộc (None, 'X', hoặc 'O')

### Các hàm chính

#### `draw_grid()`
Vẽ lưới 10x10 trên màn hình bằng cách vẽ các đường ngang và dọc.

#### `draw_markers()`
Vẽ các quân X và O trên bảng dựa vào ma trận `board`. Quân X được vẽ bằng hai đường chéo màu đỏ, quân O được vẽ bằng hình tròn màu xanh.

#### `check_win(row, col)`
Kiểm tra điều kiện thắng sau khi người chơi đặt quân tại vị trí (row, col). Hàm này kiểm tra 4 hướng:
- `check_horizontal()`: Kiểm tra 5 quân liên tiếp theo hàng ngang
- `check_vertical()`: Kiểm tra 5 quân liên tiếp theo hàng dọc
- `check_diagonal1()`: Kiểm tra 5 quân liên tiếp theo đường chéo chính (từ trái trên xuống phải dưới)
- `check_diagonal2()`: Kiểm tra 5 quân liên tiếp theo đường chéo phụ (từ phải trên xuống trái dưới)

#### `check_draw()`
Kiểm tra điều kiện hòa bằng cách xem bảng đã đầy chưa (không còn ô trống).

#### `draw_game_over()`
Hiển thị thông báo kết thúc trò chơi và hướng dẫn chơi lại. Thông báo sẽ hiển thị người thắng hoặc thông báo hòa.

#### `reset_game()`
Khởi tạo lại trò chơi bằng cách đặt lại ma trận `board`, lượt chơi, và các biến trạng thái.

#### Vòng lặp chính
Vòng lặp chính của trò chơi xử lý các sự kiện như:
- Thoát game khi nhấn nút đóng cửa sổ
- Chơi lại khi nhấn phím R sau khi trò chơi kết thúc
- Xử lý sự kiện click chuột để đặt quân
- Cập nhật và vẽ lại màn hình

## Cải tiến có thể thực hiện

- Thêm AI để chơi với máy tính
- Thêm âm thanh và hiệu ứng
- Thêm tính năng lưu và tải trò chơi
- Thêm bảng xếp hạng và thống kê
- Tùy chỉnh kích thước bảng và điều kiện thắng

## Tác giả

Game được tạo bởi người dùng thông qua Amazon Q.

## Giấy phép

Mã nguồn này được cung cấp miễn phí và có thể được sử dụng, sửa đổi và phân phối lại.
