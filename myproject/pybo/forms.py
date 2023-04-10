# pybo에 질문 등록시 사용
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

# 질문 폼 만들기
class QuestionForm(FlaskForm):
    subject = StringField('제목', validators = [DataRequired()])
    content = TextAreaField('내용', validators = [DataRequired()])
    