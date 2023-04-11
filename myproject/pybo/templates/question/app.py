import pyttsx3
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

import asyncio

if not asyncio.get_event_loop().is_running():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

tokenizer = AutoTokenizer.from_pretrained("t5-small")
model = AutoModelForSeq2SeqLM.from_pretrained("t5-small")
engine = pyttsx3.init()

def generate_speech(text):
    input_ids = tokenizer.encode(text, return_tensors="pt")
    outputs = model.generate(input_ids)
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    engine.say(generated_text)
    engine.runAndWait()
    return generated_text

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/generate_speech", methods=["POST"])
def text_to_speech():
    text = request.form["text"]
    speech_text = generate_speech(text)
    return render_template("index.html", speech_text=speech_text)

if __name__ == "__main__":
    app.run(debug=True)