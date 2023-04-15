import torch
import requests
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, render_template, request, Blueprint, url_for, g
from pybo.forms import QuestionForm
from pybo.models import Question
from werkzeug.utils import redirect
from pybo import db
from werkzeug.exceptions import BadRequestKeyError

# Load the model
tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")

grammar = Blueprint('grammar' ,__name__, url_prefix='/grammar')

# Define the homepage
@grammar.route('/')
def home():
    return render_template('question/grammar.html')

def correct_grammar(sentence):
    inputs = tokenizer.encode(sentence, return_tensors="pt") # sentence라는 input이 들어오면 토크나이징 후 inputs에 바인딩
    outputs = model.generate(inputs, max_length=1024, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=3,  num_beams=10, early_stopping=True) # 디코딩
    corrected_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_sentence

# Define the function to handle the form submission
@grammar.route('/correct_grammar', methods=['POST', 'GET'])
def correct_grammar_api():
    if request.method == 'POST':
        if 'review' in request.form:
            sentence = request.form['sentence']
            corrected_sentence = correct_grammar(sentence)
            return render_template('question/grammar.html', sentence=sentence, corrected_sentence=corrected_sentence)
        elif 'save' in request.form:
            form = QuestionForm()
            question = Question(subject=form.subject.data, content=form.content.data,
                                create_date=datetime.now(), user=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect(url_for('question._list'))
    else:
        return render_template('question/grammar.html')
