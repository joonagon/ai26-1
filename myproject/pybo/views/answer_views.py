from datetime import datetime

from flask import Blueprint, url_for, request, render_template, g
# werkzeug 툴 사용
from werkzeug.utils import redirect

from pybo import db
# 답변 폼 추가
from pybo.forms import AnswerForm
from pybo.models import Question, Answer

#  답변 블루프린트 제작
bp = Blueprint('answer', __name__, url_prefix = '/answer')

# form이 POST 방식인 bp.route 애너테이션 (똑같은 폼 형식 필요)
@bp.route('/create/<int:question_id>', methods=('POST',))
def create(question_id):
    form = AnswerForm()
    question = Question.query.get_or_404(question_id)
    if form.validate_on_submit():
        content = request.form['content']
        answer = Answer(content=content, create_date=datetime.now(), user=g.user)
        question.answer_set.append(answer)
        db.session.commit()
        return redirect(url_for('question.detail', question_id=question_id))
    return render_template('question/question_detail.html', question=question, form=form)
