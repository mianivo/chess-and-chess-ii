import pygame
from chess_board import chess_board
import time

pygame.init()


class Label:
    '''Текстовая метка на экране'''
    def __init__(self, x_cor=0, y_cor=0, text='12345', text_color=(0, 0, 0), text_size=25):
        self.text_size = text_size
        self.text_color = text_color

        self.text = text
        self.image_text = pygame.font.SysFont('arial', text_size).render(self.text, 1, text_color)
        self.text_cord = x_cor, y_cor

        self.clicked_time = 0

    def set_click_timer(self):

        self.clicked_time = time.time()

    def change_text(self, new_text):
        '''Меняет текст на кнопке'''
        self.image_text = pygame.font.SysFont('arial', self.text_size).render(new_text, 1, self.text_color)

    def draw_text(self, window):
        window.blit(self.image_text, (self.text_cord))

    def mouse_on_button(self, mouse_x, mouse_y, is_click):
        '''Совершает некое действие, при наведении мыши на метку'''
        pass


class Buttons(Label):
    '''Кнопка, имеющая текст. К метке добавляется поведение кнопки'''
    image = pygame.image.load('images\long_button.png')
    image_on = pygame.image.load('images\long_button_on.png')

    def __init__(self, x_cor=0, y_cor=0, text='12345',
                 text_color=(0, 0, 0), text_size=23, command=None, parent=None, is_active=True):
        super().__init__(x_cor, y_cor, text, text_color, text_size)
        self.command = command
        self.image_for_draw = self.image

        self.parent = parent  # При нажатии на кнопку появляются другие кнопки.
        # Кнопки которые появляюся 'дочерние'. Кнопка, которую нужно нажать чтобы другие появились 'родительская'

        self.is_active = is_active
        self.rect = self.image.get_rect()
        self.rect.x = x_cor
        self.rect.y = y_cor
        self.change_text(self.text)

    def do_command(self):
        self.command()

    def change_text(self, new_text):
        self.image_text = pygame.font.SysFont('arial', self.text_size).render(new_text, 1, self.text_color)
        text_cord_x = (self.rect.x * 2 + self.rect.width) // 2 - (self.image_text.get_rect().width // 2)
        text_cord_y = (self.rect.y * 2 + self.rect.height) // 2 - (self.image_text.get_rect().height // 2)
        self.text_cord = (text_cord_x, text_cord_y)

    def draw(self, window):
        if self.parent:
            if not self.parent.is_active:
                return None
        window.blit(self.image_for_draw, (self.rect.x, self.rect.y))
        self.draw_text(window)

    def mouse_on_button(self, mouse_x, mouse_y, is_click):
        if self.rect.collidepoint(mouse_x, mouse_y):
            if is_click and time.time() - self.clicked_time > 0.2:
                self.set_click_timer()
                self.do_command()

            self.image_for_draw = self.image_on
        else:
            self.image_for_draw = self.image


class Menu:
    '''Меню отображающее метки и кнопки на 1 поверхности.'''
    # в программе только 1 основное окно. Если бы было несколько разных разделов программы,
    # можно было бы сделать несколькор экземпляров этого класса
    def __init__(self, buttons_list=[]):
        self.buttons_list = buttons_list

    def add_button(self, new_button):
        '''добавляет кнопку'''
        self.buttons_list.append(new_button)

    def draw(self, window):
        for widget in self.buttons_list:
            widget.draw(window)

    def check_buttons(self, mouse_x, mouse_y, is_click=False):
        '''отправляет данные о мыши кнопкам'''
        for button in self.buttons_list:
            button.mouse_on_button(mouse_x, mouse_y, is_click)


new_game_button = Buttons(x_cor=20, y_cor=20, text='Начать заново', command=chess_board.start_new_game)

# команды для исполняемые при нажатии кнопок выведены в отдельные функции.
def change_is_vs_computer():
    '''Меняет пареметр. Игра против человека или программы'''
    chess_board.change_is_vs_computer()
    is_vs_computer = chess_board.get_is_vs_computer()
    if is_vs_computer:
        vs_computer.change_text('Против компьютера')
        vs_computer.is_active = True
    else:
        vs_computer.change_text('2 игрока')
        vs_computer.is_active = False
    chess_board.start_new_game()


vs_computer = Buttons(x_cor=205, y_cor=20, text='2 игрока', command=change_is_vs_computer, is_active=False)


def change_side():
    '''Меняет пареметр. Игра за черных или белых'''
    chess_board.change_side()
    if chess_board.get_side() == 'w':
        side_button.change_text('Вы за белых')
    else:
        side_button.change_text('Вы за черных')
    chess_board.start_new_game()



side_button = Buttons(x_cor=390, y_cor=20, text='Вы за белых', command=change_side, parent=vs_computer)


def change_ii_complex():
    '''Меняет пареметр сложности игры с компьютером'''
    chess_board.change_ii_complex()
    ii_complex = chess_board.get_ii_complex()
    if ii_complex == 0:
        ii_complex_button.change_text('Ходит случайно')
    elif ii_complex == 1:
        ii_complex_button.change_text('Сложность легкая')
    elif ii_complex == 2:
        ii_complex_button.change_text('Сложность средняя')
    elif ii_complex == 3:
        ii_complex_button.change_text('Сложность высокая')
    chess_board.start_new_game()


ii_complex_button = Buttons(x_cor=575, y_cor=20, text='Сложность средняя', command=change_ii_complex,
                            parent=vs_computer)


menu = Menu(buttons_list=[new_game_button, vs_computer, side_button, ii_complex_button])
