import torch
import requests
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, render_template, request, Blueprint, url_for, g
from pybo.forms import DiaryForm
from pybo.models import Diary
from werkzeug.utils import redirect
from pybo import db
import nltk
# 저장하면 주석처리
# nltk.download('punkt')

tokenizer2 = AutoTokenizer.from_pretrained("fabiochiu/t5-base-tag-generation")
model2 = AutoModelForSeq2SeqLM.from_pretrained("fabiochiu/t5-base-tag-generation")
from werkzeug.exceptions import BadRequestKeyError

# Load the model
tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")

grammar = Blueprint('grammar' ,__name__, url_prefix='/grammar')

def correct_grammar(sentence):
    inputs = tokenizer.encode(sentence, return_tensors="pt") # sentence라는 input이 들어오면 토크나이징 후 inputs에 바인딩
    outputs = model.generate(inputs, max_length=512, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=3, num_beams=5, early_stopping=True) # 디코딩
    corrected_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_sentence

def generate_tags(sentence):
    inputs = tokenizer2(sentence, max_length=512, truncation=True, return_tensors="pt")
    output = model2.generate(**inputs, num_beams=2, do_sample=True, min_length=10, max_length=32)
    decoded_output = tokenizer2.batch_decode(output, skip_special_tokens=True)[0]
    tags = list(set(decoded_output.strip().split(", ")))
    return tags

@grammar.route('/')
def index():
    # 현재 일기쓰기 프로젝트에 맞게 첫 페이지를 대체 ▼
    return render_template('index3.html')

# Define the function to handle the form submission
@grammar.route('/correct_grammar2', methods=['POST', 'GET'])
def correct_grammar_api():
    if 'save' in request.form:
        sentence = request.form['sentence']
        tags = generate_tags(sentence)
        tags = tags[:3]
        return render_template('index3.html', sentence=sentence, tags=tags) # tags 지움

    # elif 'save' in request.form:
    #     form = DiaryForm()
    #     sentence = request.form.get('sentence')
    #     tags = generate_tags(sentence)
    #     tags = tags[:3]
    #     print(tags)
    #     # save_tag = form.tags.data.replace(" ", "").split(",")
    #     # save_tag = form.tags.data.replace(" ", "").split(",")
    #     # make_str = ','.join(save_tag)
    #     # delete_enter = make_str.replace("\n", ",")
    #     diary = Diary(subject=form.subject.data, content=form.content.data,
    #                         create_date=datetime.now(), user=g.user)
    #     # , tags = delete_enter
    #     db.session.add(diary)
    #     db.session.commit()
    #     return render_template('index3.html')

