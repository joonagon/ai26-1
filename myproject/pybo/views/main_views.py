from flask import Blueprint, render_template

# 게시판 질문 목록 템플릿 준비
from pybo.models import Question

bp = Blueprint('main', __name__, url_prefix='/')

# 라우팅 함수 매핑
@bp.route('/hellopage')
def hello_pybo():
    return 'Hello0*0, Pyboooo!'

# 블루프린트에 라우팅 함수 추가-인덱스 페이지임
@bp.route('/')
def index():
    question_list = Question.query.order_by(Question.create_date.desc())
    # 템플릿 파일을 화면으로 렌더링
    return render_template('question/question_list.html', question_list=question_list)
    # return render_template('question/answer_list.html', answer_list = answer_list)


# question_list에서 요청된 url에 대응할 수 있도록 라우팅 함수 추가
@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    question = Question.query.get(question_id)
    return render_template('question/question_detail.html', question=question)