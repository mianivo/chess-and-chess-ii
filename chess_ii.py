import random
from positon_estimater import PositionEstimater


# РАзные сложности компьютера. ТУт нет высокой сложности

class ChessRandomII:
    def __init__(self):
        self.saved_positions = {}
        self.chess = None
        self.estimater = PositionEstimater()

    def get_move(self):
        return random.choice(list(self.chess.board.legal_moves))

    def set_chess(self, chess):
        self.chess = chess


class ChessEasyII:
    def __init__(self):
        self.saved_positions = {}
        self.chess = None
        self.move_count = 0
        self.estimater = PositionEstimater()

    def get_move(self):
        if self.move_count == 0:
            self.move_count += 1
            return random.choice(list(self.chess.board.legal_moves))
        best_move = self.minimax(3, True)
        self.move_count += 1
        return best_move[1]

    def set_chess(self, chess):
        self.chess = chess

    def minimax(self, depth, is_maximize_side):
        if depth == 0:
            positon_value_now = self.chess.estimate_position()
            return [positon_value_now, None]
        if is_maximize_side:
            best_move_list = [-99999, None]
            for move in self.chess.board.legal_moves:
                self.chess.board.push(move)
                new_move = self.minimax(depth - 1, not is_maximize_side)
                if new_move[0] > best_move_list[0]:
                    best_move_list = new_move
                    best_move_list[1] = move
                self.chess.board.pop()
        else:
            best_move_list = [99999, None]
            for move in self.chess.board.legal_moves:
                self.chess.board.push(move)
                new_move = self.minimax(depth - 1, not is_maximize_side)
                if new_move[0] < best_move_list[0]:
                    best_move_list = new_move
                    best_move_list[1] = move
                self.chess.board.pop()
        return best_move_list


class ChessNormalII:
    def __init__(self):
        self.saved_positions = {}
        self.chess = None
        self.move_count = 0
        self.estimater = PositionEstimater()
        self.counter = 0

    def get_move(self):
        answer = []
        for move in self.chess.board.legal_moves:
            best_move = self.minimax(4, True, -99999, 99999, [move])
            answer.append(best_move)
        answer.sort(key=lambda x: x[0])
        self.move_count += 1
        self.counter = 0
        return answer[-1][1]

    def set_chess(self, chess):
        self.chess = chess

    def get_figure_cords(self):
        answer_ii = []
        answer_enemy = []
        for figure in [1, 2, 3, 4, 5, 6]:
            answer_ii.append((figure, self.chess.board.pieces(figure, self.chess.ii_side)))
        for figure in [1, 2, 3, 4, 5, 6]:
            answer_enemy.append((figure, self.chess.board.pieces(figure, not self.chess.ii_side)))
        return answer_ii, answer_enemy

    def minimax(self, depth, is_maximize_side, alpha, beta, move_list):
        if depth <= 0:  # Если достигнут предел глубиныЮ возвращаем обычую оченку позиции на основе росположения фигур
            positon_value_now = self.estimater.smart_estimate(*self.get_figure_cords())  # оценка позиции (лист дерев)
            return [positon_value_now, None]  # возвращаем оценку, что то за ход будет определенно в цикле

        if is_maximize_side:  # Просчет для ии
            best_move_list = [-99999, None]  # Базовая оценка хода.
            for move in move_list:  # обход возможных ходов
                self.chess.board.push(move)  # совершаем ход и
                new_move = self.minimax(depth - 1, not is_maximize_side, alpha, beta,
                                        self.chess.board.legal_moves)
                if self.chess.board.is_check():  # Приоритет для шахов, чтобы ИИ заканчивал игру
                    # Иначе, если за глубину расчета он не может выиграть фигуру, он не пытается атаковать
                    new_move[0] += 65
                if new_move[0] > best_move_list[
                    0]:  # Если новый ход по оценке лучше лучшего хода на данный момент, новый ход становится лучшим
                    best_move_list = new_move
                    best_move_list[1] = move
                self.chess.board.pop()  # отменяем ход
                if alpha < best_move_list[0]:  #
                    alpha = best_move_list[0]
                if alpha >= beta:
                    return best_move_list
        else:  # Просчет для соперника
            best_move_list = [99999, None]
            for move in move_list:
                self.chess.board.push(move)
                new_move = self.minimax(depth - 1, not is_maximize_side, alpha, beta,
                                        self.chess.board.legal_moves)

                if new_move[0] < best_move_list[0]:
                    best_move_list = new_move
                    best_move_list[1] = move
                self.chess.board.pop()
                if beta > best_move_list[0]:
                    beta = best_move_list[0]
                if alpha >= beta:
                    return best_move_list

        return best_move_list
