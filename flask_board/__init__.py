import os
from flask import Flask

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY = 'dev', # 배포시 임의의 값으로 수정해야 함.
        DATABASE = os.path.join(app.instance_path, 'flask_board.sqlite'),
        #DATABASE가 INSTANCE폴더가리킴, flask_board.SQLITE 이름으로 생성하겠다
    )
    
    try:
        #lunux mkdir과 같음, 인스턴스 폴더 만들기
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello World :)'


    #database init함수
    from . import db
    db.init_app(app)

    #blueprint설정
    from . import auth
    app.register_blueprint(auth.bp)
    from . import board
    app.register_blueprint(board.bp)
    app.add_url_rule('/', endpoint='index')


    return app

