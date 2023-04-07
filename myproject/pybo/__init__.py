from flask import Flask

def create_app():
    app = Flask(__name__)

    # 블루프린트로 라우팅함수 관리함
    from .views import main_views
    app.register_blueprint(main_views.bp)

    # 플라스크 애플리케이션 팩토리를 사용해서 작성함
    # @app.route('/')
    # def hello_pybo():
    #     return "Hello! Pybooooo!"

    return app