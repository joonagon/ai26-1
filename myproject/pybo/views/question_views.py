from datetime import datetime
# 블루프린트로 기능 분리 ◀ main_views.py
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Question, Answer, User, question_voter

# 질문 등록 라우팅 함수 추가
from pybo.forms import QuestionForm, AnswerForm

bp = Blueprint('question', __name__, url_prefix = '/question')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default = 1) # 페이지 기능
    kw = request.args.get('kw', type=str, default='') # 검색 기능
    question_list = Question.query.order_by(Question.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.question_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        question_list = question_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.question_id == Question.id) \
            .filter(Question.subject.ilike(search) | # 제목
                    Question.content.ilike(search) | # 내용
                    User.username.ilike(search) |    # 작성한사람
                    sub_query.c.content.ilike(search) | # 댓글내용
                    sub_query.c.username.ilike(search) # 댓글 쓴사람
                    ) \
            .distinct()
    question_list = question_list.paginate(page=page, per_page=8)
    return render_template('question/question_list.html', question_list=question_list, page=page, kw=kw)

@bp.route('/detail/<int:question_id>/')
def detail(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    return render_template('question/question_detail.html', question=question, form=form)

# create 라우팅 함수 작성 - GET, POST을 모두 처리하고 라벨이나 입력폼 사용시 필요
@bp.route('/create/', methods=('GET','POST'))
def create():
    form = QuestionForm()
    if request.method == 'POST' and form.validate_on_submit():
        question = Question(subject=form.subject.data, content=form.content.data, create_date=datetime.now()
                            ,user=g.user)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question._list'))
    return render_template('question/question_form.html', form=form)
# @login_required  # 오류 발생으로 주석처리함

@bp.route('/modify/<int:question_id>', methods=('GET', 'POST'))
# @login_required
def modify(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('수정권한이 없습니다')
        return redirect('{}#answer_{}'.format(url_for('question.detail', question_id=question_id), answer.id))
    if request.method == 'POST':  # POST 요청
        form = QuestionForm()
        if form.validate_on_submit():
            form.populate_obj(question)
            question.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('question.detail', question_id=question_id))
    else: # GET 요청
        form = QuestionForm(obj=question)
    return render_template('question/question_form_modify.html', form=form)

@bp.route('/delete/<int:question_id>')
# @login_required
def delete(question_id):
    question = Question.query.get_or_404(question_id)
    if g.user != question.user:
        flash('삭제 권한이 없습니다')
        return redirect(url_for('question.detail', question_id = question_id))
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('question._list'))

# 게시글 추천
@bp.route('/vote/<int:question_id>/')
# @login_required
def vote(question_id):
    _question = Question.query.get_or_404(question_id)
    if g.user == _question.user:
        _question.voter.append(g.user)
        db.session.commit()
    else:
        _question.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('question.detail', question_id=question_id))

@bp.route('/review/<int:question_id>', methods=('POST',))
def review(question_id):
    question = Question.query.get_or_404(question_id)
    content = request.form['content']
    review = Answer(content=content)
    question.review_set.append(review)
    db.session.commit()
    return redirect(url_for('question.form', question_id=question_id))