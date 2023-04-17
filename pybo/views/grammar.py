import torch
import requests
from datetime import datetime
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from flask import Flask, render_template, request, Blueprint, url_for, g
from pybo.forms import QuestionForm
from pybo.models import Question
from werkzeug.utils import redirect
from pybo import db
import nltk

nltk.download('punkt')

tokenizer2 = AutoTokenizer.from_pretrained("fabiochiu/t5-base-tag-generation")
model2 = AutoModelForSeq2SeqLM.from_pretrained("fabiochiu/t5-base-tag-generation")
from werkzeug.exceptions import BadRequestKeyError

# Load the model
tokenizer = AutoTokenizer.from_pretrained("vennify/t5-base-grammar-correction")
model = AutoModelForSeq2SeqLM.from_pretrained("vennify/t5-base-grammar-correction")

grammar = Blueprint('grammar' ,__name__, url_prefix='/grammar')

def correct_grammar(sentence):
    inputs = tokenizer.encode(sentence, return_tensors="pt") # sentence라는 input이 들어오면 토크나이징 후 inputs에 바인딩
    outputs = model.generate(inputs, max_length=1024, do_sample=True, top_k=50, top_p=0.95, num_return_sequences=3, num_beams=10, early_stopping=True) # 디코딩
    corrected_sentence = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return corrected_sentence

def generate_tags(sentence):
    inputs = tokenizer2(sentence, max_length=512, truncation=True, return_tensors="pt")
    output = model2.generate(**inputs, num_beams=8, do_sample=True, min_length=10, max_length=64)
    decoded_output = tokenizer2.batch_decode(output, skip_special_tokens=True)[0]
    tags = list(set(decoded_output.strip().split(", ")))
    return tags

# Define the function to handle the form submission
@grammar.route('/correct_grammar', methods=['POST', 'GET'])
def correct_grammar_api():
    if 'review' in request.form:
        sentence = request.form['sentence']
        corrected_sentence = correct_grammar(sentence)
        tags = generate_tags(sentence)
        return render_template('question/grammar.html', sentence=sentence, corrected_sentence=corrected_sentence, tags=tags)
    elif 'save' in request.form:
        form = QuestionForm()
        sentence = request.form.get('sentence')
        sentence = str(sentence)
        tags = generate_tags(sentence)
        question = Question(subject=form.subject.data, content=form.content.data,
                            create_date=datetime.now(), user=g.user, tags = ','.join(tags))
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('question._list'))
    # else:
    #     return render_template('question/grammar.html')
