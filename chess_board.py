import pygame
from python_chess import my_chess
import os, sys

pygame.init()


def load_image(name):
    if not os.path.isfile(name):
        print(f"Файл с изображением '{name}' не найден")
        sys.exit()
    image = pygame.image.load(name)
    return image


# логика класса такая. Рисуется поле, фигуры по координатам которые дает класс игры шахмат.
# Доска отображает возможные ходы, отправляет данные о ходе, которыей хочет сделать пользователь.
# Класс получает данные о расположении фигуры и возможных ходов для этой фигуры
# То есть класс не знает ничего о шахматах. Он мог бы использоваться для игры в шашки, и ничего бы не поменялось.
class ChessBoard:
    '''Отображает доску и фигуры.'''
    def __init__(self):
        self.black_cell_color = (0, 0, 0)
        self.white_cell_color = (255, 255, 255)
        self.clicked_cell_color = (100, 100, 20)

        self.cell_size = 70
        self.cell_number = 8

        self.x_bias = 100
        self.y_bias = 90

        self.clicked_cell = None

        self.chess = my_chess

        self.possible_moves_dict = {}
        self.get_possible_moves()
        self.possible_moves_for_figure = []

        self.image_dict = {'r': 'black_rook.png', 'n': 'black_knight.png',
                           'b': 'black_elephant.png', 'q': 'black_queen.png',
                           'k': 'king_black.png', 'p': 'black_pawn.png',
                           'R': 'white_rook.png', 'N': 'white_knight.png',
                           'B': 'white_elephant.png', 'Q': 'white_queen.png',
                           'K': 'white_king.png', 'P': 'white_pawn.png'}
        images_path = 'figures/figure_images/'
        for key, value in self.image_dict.items():
            self.image_dict[key] = load_image(images_path + value)

        self.vs_computer = False

    def draw_field(self, window):
        for row in range(self.cell_number):
            for col in range(self.cell_number):
                if (row + col) % 2 == 0:
                    cell_color = self.white_cell_color
                else:
                    cell_color = self.black_cell_color
                window.fill(cell_color, (
                    self.x_bias + col * self.cell_size, self.y_bias + row * self.cell_size, self.cell_size,
                    self.cell_size))
        for i in range(1, 9):
            cords = self.x_bias - self.cell_size // 2, self.y_bias + self.cell_size * abs(8 - i) + self.cell_size // 4
            image_text = pygame.font.SysFont('arial', 36).render(str(i), 1, (0, 0, 0))
            window.blit(image_text, cords)
        for i in range(8):
            cords = self.x_bias + self.cell_size * i + self.cell_size // 3, self.y_bias+ self.cell_size * 8
            image_text = pygame.font.SysFont('arial', 36).render(chr(ord('a') + i), 1, (0, 0, 0))
            window.blit(image_text, cords)

        if self.clicked_cell:
            window.fill((150, 150, 150), (
                self.x_bias + self.clicked_cell[0] * self.cell_size,
                self.y_bias + self.clicked_cell[1] * self.cell_size, self.cell_size,
                self.cell_size))
        if self.possible_moves_for_figure:
            for x, y in self.possible_moves_for_figure:
                if (x + y) % 2 == 0:
                    possible_move_fill_color = (128, 228, 148)
                else:
                    possible_move_fill_color = (0, 100, 20)
                window.fill(possible_move_fill_color, (
                    self.x_bias + x * self.cell_size,
                    self.y_bias + y * self.cell_size, self.cell_size,
                    self.cell_size))

    def draw(self, window):
        self.draw_field(window=window)
        self.draw_chess(window)

    def draw_chess(self, window):
        for x, y, figure_name in self.chess.get_figure_list_for_draw():
            window.blit(self.image_dict[figure_name], (self.x_bias + x * self.cell_size,
                                                       self.y_bias + y * self.cell_size))

    def get_cell_cor(self, x_cor, y_cor):
        cell_x = (x_cor - self.x_bias) // self.cell_size
        cell_y = (y_cor - self.y_bias) // self.cell_size
        if 0 <= cell_x <= 7 and 0 <= cell_y <= 7:
            return cell_x, cell_y
        return -1, -1

    def cell_clicked(self, x_cor, y_cor):
        cell_cor = self.get_cell_cor(x_cor, y_cor)
        if 0 <= cell_cor[0] <= 7:
            if self.clicked_cell:
                self.do_move(self.clicked_cell, cell_cor)
            self.clicked_cell = cell_cor
            if self.clicked_cell in self.possible_moves_dict:
                self.possible_moves_for_figure = self.possible_moves_dict[self.clicked_cell]
            else:
                self.possible_moves_for_figure = []
            # Далее проверить нажатую фигуру

    def do_move(self, chess_start_pos, chess_end_pos):
        self.chess.do_move(chess_start_pos, chess_end_pos)
        self.get_possible_moves()

    def get_possible_moves(self):
        self.possible_moves_dict = self.chess.get_possible_moves_for_every_figure()

    def start_new_game(self):
        self.chess.restart_game()

    def change_is_vs_computer(self):
        self.chess.change_is_vs_computer()

    def get_is_vs_computer(self):
        return self.chess.get_is_vs_computer()

    def change_side(self):
        self.chess.change_player_side()

    def get_side(self):
        return self.chess.get_player_side()

    def change_ii_complex(self):
        self.chess.change_ii_complex()

    def get_ii_complex(self):
        return self.chess.get_ii_complex()

    def game_is_over(self):
        return bool(self.chess.get_game_result())

    def get_game_result(self):
        return self.chess.get_game_result()


chess_board = ChessBoard()
