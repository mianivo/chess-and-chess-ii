import chess

from chess_ii import ChessRandomII, ChessEasyII, ChessNormalII
from hard_ii_manager import ChessHardII
from positon_estimater import PositionEstimater
import random


class Chess:
    '''Класс реализует обработку ходов, полученние ходов от компьютера.'''

    def __init__(self):
        self.board = chess.Board()
        self.possible_moves = []
        self.player_side = 'w'

        self.ii_index = 2
        self.is_vs_computer = False
        self.ii_side = False if self.player_side == 'w' else True
        self.game_result = None
        self.positon_estimater = PositionEstimater(self.ii_side)

    def set_ii(self):
        self.ii_side = False if self.player_side == 'w' else True
        self.positon_estimater = PositionEstimater(self.ii_side)
        self.ii_complex_list = [ChessRandomII(), ChessEasyII(),
                                ChessNormalII(), ChessHardII()]
        for i in self.ii_complex_list:
            try:
                i.set_chess(self)
            except Exception:
                pass

        self.ii = self.ii_complex_list[self.ii_index]

    def get_figure_list_for_draw(self):
        answer = []
        for cell_index, figure in enumerate(str(self.board).split()):
            if figure != '.':
                x, y = self.convert_index_to_chess_board_cords(cell_index)
                answer.append([x, y, figure])
        return answer

    def convert_index_to_chess_board_cords(self, cell_index):
        x = cell_index % 8
        y = cell_index // 8
        return x, y

    def get_possible_moves_for_every_figure(self):
        answer = {}
        for move in self.board.legal_moves:
            figure_index_cord, move_index_cord = chess.parse_square(str(move)[:2]), chess.parse_square(str(move)[2:4])
            figure_cord = self.convert_index_to_chess_board_cords(figure_index_cord)
            move_cord = self.convert_index_to_chess_board_cords(move_index_cord)
            figure_cord = figure_cord[0], self.convert_y_cord_to_normal(figure_cord[1])
            move_cord = move_cord[0], self.convert_y_cord_to_normal(move_cord[1])
            if figure_cord in answer:
                answer[figure_cord].append(move_cord)
            else:
                answer[figure_cord] = [move_cord]
        return answer

    def convert_y_cord_to_normal(self, y_cor):
        return abs(7 - y_cor)

    def do_move(self, chess_start_pos, chess_end_pos):
        chess_start_index = chess_start_pos[0] + self.convert_y_cord_to_normal(chess_start_pos[1]) * 8
        chess_end_index = chess_end_pos[0] + self.convert_y_cord_to_normal(chess_end_pos[1]) * 8
        move_str = chess.square_name(chess_start_index) + chess.square_name(chess_end_index)
        try:
            move = chess.Move.from_uci(move_str)
            if not self.board.is_legal(move):
                try:
                    move_str = move_str + 'q'
                    move = chess.Move.from_uci(move_str)
                except Exception as e:
                    pass
            if self.board.is_legal(move):
                self.board.push(move)
                self.check_is_game_end()
                if self.is_vs_computer:
                    try:
                        move = self.ii.get_move()
                    except Exception as e:
                        print(e)
                    if move:
                        try:
                            self.do_move_for_ii(move)
                        except Exception as e:
                            # Если компьютер понимает, что скоро ему поставвят неизбежный мат, возвращается ход No
                            if self.ii_side:
                                self.game_result = '0-1'
                            else:
                                self.game_result = '1-0'

                    else:
                        print('ИИ пытается сделать ход None!!!')
                        if list(self.board.legal_moves):
                            self.do_move_for_ii(random.choice(list(self.board.legal_moves)))
                        else:
                            self.check_is_game_end()
                            if self.game_result:
                                return
                            else:
                                quit(
                                    'FATAL ERROR!!! ИИ делает ход None, список возможных ходов пустой, но игра не закончена')
        except ValueError as e:
            pass
        self.check_is_game_end()

    def do_move_for_ii(self, move):
        self.board.push(move)

    def check_is_game_end(self):
        game_result_str = self.board.result()
        if game_result_str != '*':
            self.game_result = game_result_str

    def get_game_result(self):
        return self.game_result

    def change_player_side(self):
        if self.player_side == 'w':
            self.player_side = 'b'
        else:
            self.player_side = 'w'

    def get_player_side(self):
        return self.player_side

    def get_ii_complex(self):
        return self.ii_index

    def change_ii_complex(self):
        self.ii_index += 1
        if self.ii_index >= len(self.ii_complex_list):
            self.ii_index = 0
        self.ii = self.ii_complex_list[self.ii_index]

    def change_is_vs_computer(self):
        self.set_ii()
        self.is_vs_computer = not self.is_vs_computer

    def get_is_vs_computer(self):
        return self.is_vs_computer

    def restart_game(self):
        self.set_ii()
        self.board = chess.Board()
        self.possible_moves.clear()
        self.game_result = None
        if self.is_vs_computer:
            self.ii_side = False if self.player_side == 'w' else True
            if self.player_side == 'b':
                move = self.ii.get_move()
                self.do_move_for_ii(move)

    def get_figure_cords(self):
        answer_ii = []
        answer_enemy = []
        for figure in [1, 2, 3, 4, 5, 6]:
            answer_ii.append((figure, self.board.pieces(figure, self.ii_side)))
        for figure in [1, 2, 3, 4, 5, 6]:
            answer_enemy.append((figure, self.board.pieces(figure, not self.ii_side)))
        return answer_ii, answer_enemy

    def estimate_position(self):
        return self.positon_estimater.estimate_position(*self.get_figure_cords())

    def smart_estimate_position(self):
        return self.positon_estimater.smart_estimate(*self.get_figure_cords())


my_chess = Chess()
my_chess.get_possible_moves_for_every_figure()
