import sqlite3
import torch
import requests
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, render_template, request




grammar = Flask(__name__)





tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")



# db생성 함수
def create_db():
    conn = sqlite3.connect('sentences.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE sentences
    (sentence1 text, sentence2 text, sentence3 text, sentence4 text, sentence5 text,
    sentence6 text, sentence7 text, sentence8 text, sentence9 text, sentence10 text)''')  # 필요에따라 컬럼 늘릴수있ㅇ므
    conn.commit()
    conn.close()


def correct_grammar(sentence):
    inputs = tokenizer.encode(sentence, return_tensors="pt")
    outputs = model.generate(inputs, max_length=1024, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=3, num_beams=10, early_stopping=True)
    corrected_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_sentence


@grammar.route('/')
def home():
    return render_template('grammar.html')


@grammar.route('/correct_grammar', methods=['POST'])
def correct_grammar_api():
    sentence = request.form['sentence']
    corrected_sentence = correct_grammar(sentence)
    conn = sqlite3.connect('sentences.db')
    c = conn.cursor()
    values = corrected_sentence.split()[:10] + ['']*(10-len(corrected_sentence.split()[:10]))
    # corrected_sentence.split()[:10] 문장을 10개까지 슬라이싱
    # ['']*(10-len(corrected_sentence.split()[:10]))
    # 사용자가 입력한 문장이 10개 미만이면 나머지 컬럼들은 빈리스트 ['']로 채움 padding..
    # 그리고 둘을 더해서 결과적으로 사용자가 영어 문장을 입려하면 단어별로 쪼개서 컬럼에 순서대로 채우되 자른문장 < len(column) 이면 나머지 는 빈 값으로 채움

    c.execute("INSERT INTO sentences VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", values)
    # ? placeholder
    # sentences 라는 db에 위에서 선언한 변수 values의 값들이 순서대로 들어감 sentence1부터 ~
    conn.commit()
    conn.close()
    return render_template('grammar.html', sentence=sentence, corrected_sentence=corrected_sentence)

@grammar.route('/sentences', methods=['GET'])
def get_sentences():
    # DB 연결
    conn = sqlite3.connect('sentences.db')
    c = conn.cursor()

    # sqlite3의 select 문법이 execute
    #
    c.execute("SELECT sentence1, sentence2, sentence3, sentence4, sentence5, sentence6, sentence7, sentence8, sentence9, sentence10 FROM sentences")

    # 조회 결과 출력
    # 쿼리 실행 결과를 튜플의 리스트 형태로 반환
    rows = c.fetchall()

    # DB 연결 종료
    conn.close()

    return render_template('sentences.html', rows=rows)

if __name__ == '__main__':
    # create_db()
    grammar.run(debug=True)