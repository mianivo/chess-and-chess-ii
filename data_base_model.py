import sqlalchemy


from db_sess import SqlAlchemyBase


class Games(SqlAlchemyBase):
    __tablename__ = 'games'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    is_white_move = sqlalchemy.Column(sqlalchemy.Boolean)
    str_board = sqlalchemy.Column(sqlalchemy.String, index=True)
    move = sqlalchemy.Column(sqlalchemy.String)

