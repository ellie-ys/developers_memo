import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        #g.DB에 커넥션 객체
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            #파일경로
            detect_types=sqlite3.PARSE_DECLTYPES
            #두번째 인자 , 뭐지?
        )
        g.db.row_factory = sqlite3.Row
        #튜플이라KEY값 못꺼내는데
        #  SQLITE3.ROW객체(꺼낼 수 있도록)
    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
        

def init_db():
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


#init-db명령어 치면 init-db함수 호출되도록
@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
    

def init_app(app):
    #app끝날 때 실행할 함수 추가, db연결없애도록하는 함수 추가
    app.teardown_appcontext(close_db)
    #실행시킨 app에 명령어 추가
    app.cli.add_command(init_db_command)