from flask import Blueprint

bp = Blueprint('main', __name__, url_prefix='/')

# 라우팅 함수 매핑
@bp.route('/hellopage')
def hello_pybo():
    return 'Hello0*0, Pyboooo!'

# 블루프린트에 라우팅 함수 추가-인덱스 페이지임
@bp.route('/')
def index():
    return 'Pybo Index'