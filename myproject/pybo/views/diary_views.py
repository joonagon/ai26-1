from datetime import datetime
# 블루프린트로 기능 분리 ◀ main_views.py
from flask import Blueprint, render_template, request, url_for, g, flash
from werkzeug.utils import redirect

from pybo import db
from pybo.models import Diary, Answer, User, diary_voter

# 질문 등록 라우팅 함수 추가
from pybo.forms import DiaryForm, AnswerForm

bp = Blueprint('diary', __name__, url_prefix = '/diary')

@bp.route('/list/')
def _list():
    page = request.args.get('page', type=int, default = 1) # 페이지 기능
    kw = request.args.get('kw', type=str, default='') # 검색 기능
    diary_list = Diary.query.order_by(Diary.create_date.desc())
    if kw:
        search = '%%{}%%'.format(kw)
        sub_query = db.session.query(Answer.diary_id, Answer.content, User.username) \
            .join(User, Answer.user_id == User.id).subquery()
        diary_list = diary_list \
            .join(User) \
            .outerjoin(sub_query, sub_query.c.diary_id == Diary.id) \
            .filter(Diary.subject.ilike(search) | # 제목
                    Diary.content.ilike(search) | # 내용
                    Diary.tags.ilike(search) | # 태그까지
                    User.username.ilike(search) |    # 작성한사람
                    sub_query.c.content.ilike(search) | # 댓글내용
                    sub_query.c.username.ilike(search) # 댓글 쓴사람
                    ) \
            .distinct()
    diary_list = diary_list.paginate(page=page, per_page=8)
    return render_template('diary/diary_list.html', diary_list=diary_list, page=page, kw=kw)

@bp.route('/detail/<int:diary_id>/')
def detail(diary_id):
    form = AnswerForm()
    diary = Diary.query.get_or_404(diary_id)
    return render_template('diary/diary_detail.html', diary=diary, form=form)

# create 라우팅 함수 작성 - GET, POST을 모두 처리하고 라벨이나 입력폼 사용시 필요
@bp.route('/create/', methods=('GET','POST'))
def create():
    form = DiaryForm()
    if request.method == 'POST' and form.validate_on_submit():
        diary = Diary(subject=form.subject.data, content=form.content.data, create_date=datetime.now()
                            ,user=g.user, tags=form.tags.data)
        db.session.add(diary)
        db.session.commit()
        return redirect(url_for('diary._list'))
    return render_template('diary/diary_form.html', form=form)
# @login_required  # 오류 발생으로 주석처리함

@bp.route('/modify/<int:diary_id>', methods=('GET', 'POST'))
# @login_required
def modify(diary_id):
    diary = Diary.query.get_or_404(diary_id)
    if g.user != diary.user:
        flash('수정권한이 없습니다')
        return redirect('{}#answer_{}'.format(url_for('diary.detail', diary_id=diary_id), answer.id))
    if request.method == 'POST':  # POST 요청
        form = DiaryForm()
        if form.validate_on_submit():
            form.populate_obj(diary)
            diary.modify_date = datetime.now()  # 수정일시 저장
            db.session.commit()
            return redirect(url_for('diary.detail', diary_id=diary_id))
    else: # GET 요청
        form = DiaryForm(obj=diary)
    return render_template('diary/diary_form_modify.html', form=form)

@bp.route('/delete/<int:diary_id>')
# @login_required
def delete(diary_id):
    diary = Diary.query.get_or_404(diary_id)
    if g.user != diary.user:
        flash('삭제 권한이 없습니다')
        return redirect(url_for('diary.detail', diary_id = diary_id))
    db.session.delete(diary)
    db.session.commit()
    return redirect(url_for('diary._list'))

# 게시글 추천
@bp.route('/vote/<int:diary_id>/')
# @login_required
def vote(diary_id):
    _diary = Diary.query.get_or_404(diary_id)
    if g.user == _diary.user:
        _diary.voter.append(g.user)
        db.session.commit()
    else:
        _diary.voter.append(g.user)
        db.session.commit()
    return redirect(url_for('diary.detail', diary_id=diary_id))

@bp.route('/review/<int:diary_id>', methods=('POST',))
def review(diary_id):
    diary = Diary.query.get_or_404(diary_id)
    content = request.form['content']
    review = Answer(content=content)
    diary.review_set.append(review)
    db.session.commit()
    return redirect(url_for('diary.form', diary_id=diary_id))