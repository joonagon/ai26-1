from pybo import db

# 리비전 파일이 자동으로 업그레이드
class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(400), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_date= db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref = db.backref('question_set'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    question = db.relationship('Question', backref = db.backref('answer_set', cascade = 'all, delete-orphan'))
    content = db.Column(db.Text(), nullable = False)
    create_date = db.Column(db.DateTime(), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    user = db.relationship('User', backref=db.backref('answer_set'))

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(150), unique=True, nullable = False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    nickname = db.Column(db.String(400))
    name = db.Column(db.String(150), nullable=False)
    dayofbirth = db.Column(db.String(200), nullable=False)

# 공지사항
class Notice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(400), nullable=False)
    content = db.Column(db.Text(), nullable=False)
