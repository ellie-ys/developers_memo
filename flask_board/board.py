from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flask_board.auth import login_required
from flask_board.db import get_db

# 게시판 board 블루프린트 생성! 기본값으로 /board URL을 사용합니다.
bp = Blueprint('board', __name__)

# /board URL로 접속시
@bp.route('/')
def index():
    # db의 정보를 가져옵니다.
    db = get_db()
    
    # 게시글 정보를 모두 가져오는 query를 실행
    boards = db.execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM board p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    
    return render_template('board/index.html', boards=boards)


@bp.route('/create', methods=('GET', 'POST'))
# auth.py에서 작성한 login_required() 함수를 데코레이터로 호출
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = '제목이 유효하지 않습니다.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO board (title, body, author_id)'
                ' VALUES (?, ?, ?)',
                (title, body, g.user['id'])
            )
            db.commit()
            return redirect(url_for('board.index'))

    return render_template('board/create.html')



def get_board(id, check_author=True):
    board = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM board p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    
    # 게시글의 정보가 존재 하지 않을 때, 404 에러를 발생시킵니다.
    if board is None:
        abort(404, "게시글 {0}가 존재하지 않습니다.".format(id))


    # check_author가 False로 변경된다면, 누구나 게시글을 수정할 수 있도록 변경할 수 있습니다.
    if check_author and board['author_id'] != g.user['id']:
        abort(403)

    return board


# /board/게시글id/update 주소를 받았을 때 동작합니다. GET,POST 요청을 모두 받습니다.
@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    # 전달받은 id에 해당하는 게시글 정보를 가져옵니다.
    board = get_board(id)
    
    # POST 요청을 받았다면?
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = '제목이 유효하지 않습니다.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE board SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('board.index'))

    return render_template('board/update.html', board=board)


# /board/게시글id/delete 주소로 접속했을 때 동작합니다. POST 요청을 받습니다.
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_board(id)
    db = get_db()
    db.execute('DELETE FROM board WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('board.index'))