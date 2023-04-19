from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import sqlite3
import torch
import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, render_template, request

tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")

grammar = Flask(__name__)

# sqlalchemy 사용 할 때 필요
engine = create_engine('sqlite:///sentences.db', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# db 만들기
class Sentence(Base):
    __tablename__ = 'sentences'
    id = Column(Integer, primary_key=True)
    sentence1 = Column(String)
    sentence2 = Column(String)
    sentence3 = Column(String)
    sentence4 = Column(String)
    sentence5 = Column(String)
    sentence6 = Column(String)
    sentence7 = Column(String)
    sentence8 = Column(String)
    sentence9 = Column(String)
    sentence10 = Column(String)

# 위에 테이블 만드는 함수
Base.metadata.create_all(engine)

# sqlite3 -> sqlalchemy 로 변경하면서 사용 안함
# def create_db():
#
#     pass

def correct_grammar(sentence):
    inputs = tokenizer.encode(sentence, return_tensors="pt")
    outputs = model.generate(inputs, max_length=1024, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=3, num_beams=5, early_stopping=True)
    corrected_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_sentence


# index 페이지
@grammar.route('/')
def home():
    return render_template('grammar.html')


@grammar.route('/correct_grammar', methods=['POST'])
def correct_grammar_api():
    sentence = request.form['sentence'] # 사용자 입력값을 받아서
    corrected_sentence = correct_grammar(sentence) # model serving 함수에 인자로 넣음

    # DB에 연결할 때 해야함
    session = Session()

    # 스페이스바 기준으로 단어를 자르고 10개까지만 db에 넣음 + 잘린 단어가 10개보다 아래면 나머지는 '' (공백)으로 db에 채워짐
    values = sentence.split()[:10] + ['']*(10-len(sentence.split()[:10]))
    sentence_obj = Sentence(sentence1=values[0], sentence2=values[1], sentence3=values[2], sentence4=values[3], sentence5=values[4],
                            sentence6=values[5], sentence7=values[6], sentence8=values[7], sentence9=values[8], sentence10=values[9])

    # 세션에 추가
    session.add(sentence_obj)

    # commit 하면 db에 저장
    session.commit()

    #
    session.close()

    return render_template('grammar.html', sentence=sentence, corrected_sentence=corrected_sentence)

# db 화면에 출력
@grammar.route('/sentences', methods=['GET'])
def get_sentences():
    # db 연결 국룰
    session = Session()

    # sql 쿼리 select * from 테이블 ; 이 sqlalchemy ORM 에서는
    # session.query(테이블명).all() 임
    # session.query(테이블명).fillter(id=1) etc..
    sentences = session.query(Sentence).all()
    # for문 돌려서
    rows = [(s.sentence1, s.sentence2, s.sentence3, s.sentence4, s.sentence5, s.sentence6, s.sentence7, s.sentence8, s.sentence9, s.sentence10) for s in sentences]


    session.close()

    return render_template('sentences.html', rows=rows)

if __name__ == '__main__':
    grammar.run(debug=True)