import os
from flask import Flask

def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev', # 배포시 임의의 값으로 수정해야 함.
        DATABASE=os.path.join(app.instance_path, 'flask_board.sqlite'),
    )
    
    try:
        #lunux mkdir과 같음, 인스턴스 폴더 만들기
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return 'Hello, Ellie!'

    return app