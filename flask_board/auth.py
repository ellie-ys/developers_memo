import functools

from flask import Blueprint
from flask import flash
from flask import g
from flask import redirect
from flask import render_template
from flask import request
from flask import session
from flask import url_for
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from flask_board.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")

# /register 주소에서 GET과 POST 메소드 방식의 요청을 모두 받음
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
                
        if not username:
            error = 'Username이 유효하지 않습니다.'
        elif not password:
            error = 'Password가 유효하지 않습니다.'
        elif db.execute(
            'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = '{} 계정은 이미 등록된 계정입니다.'.format(username)
                        
        if error is None:
            db.execute(
                'INSERT INTO user (username, password) VALUES (?, ?)',
                (username, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
    # return 'hello register'
    return render_template('auth/register.html')



@bp.route('/login', methods=('GET', 'POST'))
def login():
    if g.user is not None:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = '등록되지 않은 계정입니다.'
        elif not check_password_hash(user['password'], password):
            error = 'password가 틀렸습니다.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


# 웹 애플리케이션의 모든 요청을 받기 전에 실행
@bp.before_app_request
def load_logged_in_user():
    # 현재 session에 등록된 유저의 정보 획득
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()


def login_required(view):
    # 로그인이 필요한 기능을 사용할 때, 데코레이터로 동작
    # 로그인만 한 사람에게만 보여주는 View에서 동작
    # 로그인이 되어 있지 않다면 login 페이지로 이동
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view
    
@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
    
    