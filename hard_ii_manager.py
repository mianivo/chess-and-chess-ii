import subprocess
import chess
import time
import data_base_manager
import random


class ChessHardII:
    '''Класс реализует общение с программой отвечающей за сложный ИИ'''
    def __init__(self):
        from main import update_window
        self.saved_positions = {}
        # Спиок полей в приоритетет (центральные поля) и другие параметры будут зраниться тут
        self.chess = None
        self.update_window = update_window

        self.move_count = 19

    def get_saved_move(self, str_board, is_white):
        move = data_base_manager.get_game_from_board(str_board, is_white)
        return move

    def get_move(self):
        start_time = time.time()
        with open('hard_ii_move.txt', 'w') as f:
            pass
        saved_move = self.get_saved_move(str(self.chess.board), self.chess.ii_side)

        if saved_move:
            self.chess.smart_estimate_position()
            self.move_count += 1
            return chess.Move.from_uci(saved_move)
        else:
            if self.move_count == 0:
                if self.chess.ii_side:
                    first_ii_move = ['e2e4', 'd2d4']
                else:
                    first_ii_move = ['e7e5', 'd7d5']
                self.move_count += 1
                return chess.Move.from_uci(random.choice(first_ii_move))

        p = subprocess.Popen(
            ['python', "chess_hard_ii.py", self.chess.board.fen(), str(int(self.chess.ii_side))])

        while True:
            time.sleep(0.23)
            self.update_window(think_time=time.time() - start_time)
            with open('hard_ii_move.txt', 'r') as f:
                file_input = f.read()
                if file_input:
                    self.move_count += 1
                    return chess.Move.from_uci(file_input)

    def set_chess(self, chess):
        self.chess = chess
