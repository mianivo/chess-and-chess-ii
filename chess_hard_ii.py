from positon_estimater import PositionEstimater


class ChessHardII:
    def __init__(self, ii_side):
        self.saved_positions = {}
        # Спиок полей в приоритетет (центральные поля) и другие параметры будут зраниться тут
        self.board = None
        self.estimater = PositionEstimater()
        self.ii_side = ii_side

        self.search_depth = 4

    def get_move(self, move_list):
        '''получает лучший ход и записывает его в файл'''
        best_move = self.minimax(self.search_depth, True, -99999, 99999, move_list)
        with open('answer_move.txt', encoding='utf8', mode='a') as f:
            f.write(str(best_move[0]) + '@' + str(best_move[1]) + '\n')

    def set_chess(self, chess):
        '''задает доску'''
        self.board = chess

    def get_figure_cords(self):
        '''Возвращает положение фигур на доске'''
        answer_ii = []
        answer_enemy = []
        for figure in [1, 2, 3, 4, 5, 6]:
            answer_ii.append((figure, self.board.pieces(figure, self.ii_side)))
        for figure in [1, 2, 3, 4, 5, 6]:
            answer_enemy.append((figure, self.board.pieces(figure, not self.ii_side)))
        return answer_ii, answer_enemy

    def move_is_cut(self, move, attackers_side=True):
        '''проверяет, является ли ход взятием'''
        move_end_cord = move.to_square
        figure_in_end_cord = self.board.piece_at(move_end_cord)
        if figure_in_end_cord is not None:
            if figure_in_end_cord.color != attackers_side:
                return True
        return False

    def minimax(self, depth, is_maximize_side, alpha, beta, move_list, check_and_cut_depth=0, move_is_cut=False):
        '''алгоритм минимакс'''
        if depth <= 0 and (check_and_cut_depth >= 2 or not move_is_cut):  # Если достигнут предел глубиныЮ возвращаем обычую оченку позиции на основе росположения фигур
            positon_value_now = self.estimater.smart_estimate(*self.get_figure_cords())  # оценка позиции (лист дерев)
            return [positon_value_now, None]  # возвращаем оценку, что то за ход будет определенно в цикле

        if is_maximize_side:  # Просчет для ии
            best_move_list = [-99999, None]  # Базовая оценка хода.
            for move in move_list:  # обход возможных ходов
                move_is_cut = self.move_is_cut(move, self.ii_side)
                self.board.push(move)  # совершаем ход и
                if move_is_cut or self.board.is_check():
                    new_move = self.minimax(depth - 1, not is_maximize_side, alpha, beta,
                                            self.board.legal_moves, (check_and_cut_depth + 1) if depth <= 0 else check_and_cut_depth, move_is_cut)
                else:
                    new_move = self.minimax(depth - 1, not is_maximize_side, alpha, beta,
                                            self.board.legal_moves, check_and_cut_depth, move_is_cut)
                    # и определяем ценность хода
                if self.board.is_check():  # Приоритет для шахов, чтобы ИИ заканчивал игру
                    # Иначе, если за глубину расчета он не может выиграть фигуру, он не пытается атаковать
                    new_move[0] += 65
                if new_move[0] > best_move_list[
                    0]:  # Если новый ход по оценке лучше лучшего хода на данный момент, новый ход становится лучшим
                    best_move_list = new_move
                    best_move_list[1] = move
                self.board.pop()  # отменяем ход
                if alpha < best_move_list[0]:
                    alpha = best_move_list[0]
                if alpha >= beta:
                    return best_move_list
        else:  # Просчет для соперника
            best_move_list = [99999, None]
            for move in move_list:
                move_is_cut = self.move_is_cut(move, not self.ii_side)
                self.board.push(move)
                if move_is_cut or self.board.is_check():
                    new_move = self.minimax(depth- 1, not is_maximize_side, alpha, beta,
                                            self.board.legal_moves, (check_and_cut_depth + 1) if depth <= 0 else check_and_cut_depth, move_is_cut)
                else:
                    new_move = self.minimax(depth - 1, not is_maximize_side, alpha, beta,
                                            self.board.legal_moves, check_and_cut_depth, move_is_cut)

                if new_move[0] < best_move_list[0]:
                    best_move_list = new_move
                    best_move_list[1] = move
                self.board.pop()
                if beta > best_move_list[0]:
                    beta = best_move_list[0]
                if alpha >= beta:
                    return best_move_list

        return best_move_list


if __name__ == '__main__':
    import sys
    import multiprocessing as mpr
    import chess
    import random
    import time

    with open('answer_move.txt', encoding='utf8', mode='w') as f:
        pass

    process_count = 4  # числопроцессов, которые будут задействованы для обработки ходов.
    str_board_fen = sys.argv[1]  # передается расположение фигур на доске
    ii_is_white = int(sys.argv[2])  # за какую сторону играет программа
    start_board = chess.Board(str_board_fen)



    moves_list = list(start_board.legal_moves)
    list_len = len(moves_list)
    if list_len < process_count:
        process_count = list_len

    process_list = []
    for i in range(process_count):  # начинаем процессы
        hard_ii = ChessHardII(ii_is_white)
        hard_ii.set_chess(start_board.copy())
        p = mpr.Process(target=hard_ii.get_move, args=(
            [moves_list.pop()], ))
        p.start()
        process_list.append(p)


    def get_best_move():
        best_move = -999999
        answer = []
        with open('answer_move.txt', encoding='utf8', mode='r') as f:
            file_text = f.read()
            move_with_priority = [stri.split('@') for stri in file_text.strip().split()]
            for prority, str_move in move_with_priority:
                prority = int(prority)
                if prority > best_move:
                    answer.clear()
                    answer.append(str_move)
                    best_move = prority
                elif prority == best_move:
                    answer.append(str_move)
        try:
            return random.choice(answer)
        except IndexError:
            return


    flag = True
    while True:
        for process in process_list:  # если процесс завершился, даем ему новый ход
            if not process.is_alive():
                if moves_list:
                    hard_ii = ChessHardII(ii_is_white)
                    hard_ii.set_chess(start_board.copy())
                    p = mpr.Process(target=hard_ii.get_move, args=([moves_list.pop()], ))
                    p.start()
                    process_list.append(p)
                else:
                    if not any(map(lambda x:x.is_alive(), process_list)):
                        flag = False
        time.sleep(0.4)
        if not flag:
            break

    with open('hard_ii_move.txt', encoding='utf8', mode='w') as f:
        best_move = get_best_move()
        f.write(best_move)

