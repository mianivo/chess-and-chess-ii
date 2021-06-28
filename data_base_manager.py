import db_sess
from data_base_model import Games

db_sess.global_init('saved_boards.sqlite')


def get_game_from_board(str_board, is_white):
    '''подается ход, если оен хранится в базе данных, возвращает ход'''
    db_s = db_sess.create_session()
    game = db_s.query(Games).filter(Games.str_board == str_board).filter(Games.is_white_move == is_white).first()
    if game:
        return game.move
    return None

