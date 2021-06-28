class PositionEstimater:
    '''Возвращает оценку конкретной позиции на доске'''
    def __init__(self, ii_side='b'):
        # приоритеты фигур
        self.ii_priority_dict = {1: 100, 2: 320, 3: 330, 4: 500, 5: 905, 6: 9000}
        self.enemy_priority_dict = {1: 100, 2: 320, 3: 330, 4: 500, 5: 900, 6: 9000}

        self.ii_side = False if ii_side == 'b' else True

        # Списки, в которых хранятся позиции, на которой приоритет фигуры выше или ниже.
        self.king_pos_value_list = [-30, -40, -40, -50, -50, -40, -40, -30,
                                    -30, -40, -40, -50, -50, -40, -40, -30,
                                    -30, -40, -40, -50, -50, -40, -40, -30,
                                    -30, -40, -40, -50, -50, -40, -40, -30,
                                    -20, -30, -30, -40, -40, -30, -30, -20,
                                    -10, -20, -20, -20, -20, -20, -20, -10,
                                    20, 20, 0, 0, 0, 0, 20, 20,
                                    20, 30, 10, 0, 0, 10, 30, 20]

        self.queen_pos_value_list = [-20, -10, -10, -5, -5, -10, -10, -20,
                                    -10, 0, 0, 0, 0, 0, 0, -10,
                                    -10, 0, 5, 5, 5, 5, 0, -10,
                                    -5, 0, 5, 5, 5, 5, 0, -5,
                                    0, 0, 5, 5, 5, 5, 0, -5,
                                    -10, 5, 5, 5, 5, 5, 0, -10,
                                    10, 0, 0, 0, 0, 0, 0, -10,
                                    -20, -10, -10, -5, -5, -10, -10, -20]

        self.rook_pos_value_list = [0, 0, 0, 0, 0, 0, 0, 0,
                                     5, 10, 10, 10, 10, 10, 10, 5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    -5, 0, 0, 0, 0, 0, 0, -5,
                                    0, 0,10, 40, 30, 40, 0, 0]

        self.bishop_pos_value_list = [-20, -10, -10, -10, -10, -10, -10, -20,
                                    -10, 0, 0, 0, 0, 0, 0, -10,
                                    -10, 0, 5, 10, 10, 5, 0, -10,
                                    -10, 5, 5, 10, 10, 5, 5, -10,
                                    -10, 0, 10, 10, 10, 10, 0, -10,
                                    -10, 10, 10, 10, 10, 10, 10, -10,
                                    -10, 5, 0, 0, 0, 0, 5, -10,
                                    -20, -10, -10, -10, -10, -10, -10, -20]

        self.knight_pos_value_list = [-50, -40, -30, -30, -30, -30, -40, -50,
                                      -40, -20, 0, 0, 0, 0, -20, -40,
                                      -30, 0, 10, 15, 15, 10, 0, -30,
                                      -30, 5, 15, 20, 20, 15, 5, -30,
                                      -30, 0, 15, 20, 20, 15, 0, -30,
                                      -30, 5, 20, 15, 15, 20, 5, -30,
                                      -40, -20, 0, 5, 5, 0, -20, -30,
                                      -50, -40, -30, -30, -30, -30, -40, -50]

        self.pawn_pos_value_list = [0, 0, 0, 0, 0, 0, 0, 0,
                                    50, 50, 50, 50, 50, 50, 50, 50,
                                      10, 10, 20, 30, 30, 20, 10, 10,
                                      5, 5, 10, 25, 25, 10, 5, 5,
                                      0, 0, 0, 20, 20, 0, 0, 0,
                                      5, -5, -10, 0, 0, -10, -5, 5,
                                      5, 10, 10, -20, -20, 10, 10, 5,
                                      0, 0, 0, 0, 0, 0, 0, 0]

        self.white_priorities_dict = {1: self.pawn_pos_value_list.copy(), 2: self.knight_pos_value_list.copy(),
                                3: self.bishop_pos_value_list.copy(), 4:self.rook_pos_value_list.copy(),
                                5:self.queen_pos_value_list.copy(), 6: self.king_pos_value_list.copy()}
        self.black_priorities_dict = {1: list(reversed(self.pawn_pos_value_list.copy())), 2: list(reversed(self.knight_pos_value_list.copy())),
                                      3: list(reversed(self.bishop_pos_value_list.copy())), 4:list(reversed(self.rook_pos_value_list.copy())),
                                      5:list(reversed(self.queen_pos_value_list.copy())), 6: list(reversed(self.king_pos_value_list.copy()))}

        if self.ii_side:
            self.ii_pos_priorities_dict = self.white_priorities_dict
            self.enemy_pos_priority_dict = self.black_priorities_dict
        else:
            self.ii_pos_priorities_dict = self.black_priorities_dict
            self.enemy_pos_priority_dict = self.white_priorities_dict



    def estimate_position(self, ii_figure_list, enemy_figure_list):
        '''Возвращает оценку позиции только на основе фигур, без учета их расположения'''
        total_ii_value = 0
        total_enemy_value = 0
        for figure, figure_pos_list in ii_figure_list:
            total_ii_value += len(figure_pos_list) * self.ii_priority_dict[figure]
        for figure, figure_pos_list in enemy_figure_list:
            total_enemy_value += len(figure_pos_list) * self.enemy_priority_dict[figure]
        return total_ii_value - total_enemy_value

    def smart_estimate(self, ii_figure_list, enemy_figure_list):
        '''Возвращает оценку позиции только на основе фигур, с учетом их расположения'''
        total_ii_value = 0
        total_enemy_value = 0
        for figure_int, figure_pos_list in ii_figure_list:
            for figure_pos in figure_pos_list:
                total_ii_value += self.ii_priority_dict[figure_int] + self.ii_pos_priorities_dict[figure_int][figure_pos]
        for figure_int, figure_pos_list in enemy_figure_list:
            for figure_pos in figure_pos_list:
                total_enemy_value += self.enemy_priority_dict[figure_int] + self.enemy_pos_priority_dict[figure_int][figure_pos]
        return total_ii_value - total_enemy_value
