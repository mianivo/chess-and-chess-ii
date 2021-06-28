import time

import pygame
import settings

# Необходимо заранее инициализировать окно для корректной работы модулей
st = settings.Settings()
main_window = pygame.display.set_mode((st.window_width, st.window_height))


def update_window(think_time=0.0):
    '''Функция нужна для обновения окна игры, при прерывании основного цикла (когда программа долго думает)'''

    int_part, float_part = str(think_time).split('.')
    game.update_window(main_cycle=False, think_time=int_part + ('.' + float_part[0]) if float_part else '')


import buttons
import chess_board


class Game:
    '''Отрисовка экрана, основной цикл игры.'''
    def __init__(self):
        st = settings.Settings()  # Самые основные настройки
        self.window = main_window
        pygame.display.set_caption('Шахматы')
        self.bg = st.bg
        self.level_now = None
        self.level_go = False
        self.music_on = True

        self.chess_board = chess_board.chess_board

        self.menu = buttons.menu

        self.image_game_end_text = []
        for text in ['Игра окончена. Победили черные.', 'Игра завершена. Ничья!', 'Игра окончена Белые победили.']:
            image_text = pygame.font.SysFont('arial', 50).render(text, 1, (46, 200, 188))
            self.image_game_end_text.append(image_text)

    def update_window(self, main_cycle=True, think_time='0.0'):
        self.window.fill((140, 140, 140))
        self.chess_board.draw(window=self.window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_game()
            if main_cycle:
                mouse_pressed_keys = pygame.mouse.get_pressed()
                mouse_pos = pygame.mouse.get_pos()
                if any(mouse_pressed_keys):
                    self.chess_board.cell_clicked(*mouse_pos)
        if main_cycle:
            mouse_pressed_keys = pygame.mouse.get_pressed()
            mouse_pos = pygame.mouse.get_pos()
            self.menu.check_buttons(*mouse_pos, any(mouse_pressed_keys))
            self.menu.draw(self.window)
        else:
            self.ii_thing_image_text = pygame.font.SysFont('arial', 36).render(f'Программа "думает". Прошло {think_time} секунд', 1, (46, 200, 188))
            self.window.blit(self.ii_thing_image_text, (100, 30))
        if self.chess_board.game_is_over():
            if self.chess_board.get_game_result() == '1-0':
                image_text = self.image_game_end_text[2]
            elif self.chess_board.get_game_result() == '0-1':
                image_text = self.image_game_end_text[0]
            else:
                image_text = self.image_game_end_text[1]
            self.window.blit(image_text, (50, 330))
        pygame.display.update()
        time.sleep(0.08)


    def run_game(self):
        while True:
            self.update_window()

    def close_game(self):
        quit('Выход крестиком')


game = Game()
game.run_game()
