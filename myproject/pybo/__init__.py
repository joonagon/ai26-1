
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
    from .views import main_views, question_views, answer_views, auth_views
    app.register_blueprint(main_views.bp)
    # 블루프린트에 question_views도 적용
    app.register_blueprint(question_views.bp)
    # 답변 기능을 위한 블루프린트 등록
    app.register_blueprint(answer_views.bp)
    # 회원가입 기능을 위한 블루프린트 등록
    app.register_blueprint(auth_views.bp)
    # 필터
    from .filter import format_datetime
    app.jinja_env.filters['datetime'] = format_datetime
    return app