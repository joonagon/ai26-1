
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

import config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)  # flask 뷰 기본
    
    # ORM을 적용하기 위해서 SQLite와 SQLAlchemy 사용
    app.config.from_object(config)

    #  ORM
    db.init_app(app)
    migrate.init_app(app, db)
    from . import models

    # 블루프린트로 라우팅함수 관리함
    from .views import main_views
    app.register_blueprint(main_views.bp)

    # 플라스크 애플리케이션 팩토리를 사용해서 작성함
    # @app.route('/')
    # def hello_pybo():
    #     return "Hello! Pybooooo!"

    return app