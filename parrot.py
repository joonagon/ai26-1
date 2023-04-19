from flask import Flask, render_template, request
from transformers import T5Tokenizer, T5ForConditionalGeneration

parrot = Flask(__name__)

tokenizer = T5Tokenizer.from_pretrained('prithivida/parrot_paraphraser_on_T5')
model = T5ForConditionalGeneration.from_pretrained('prithivida/parrot_paraphraser_on_T5')

@parrot.route('/parrot')
def index():
    return render_template('index.html')

@parrot.route('/parrot', methods=['POST'])
def get_paraphrase():
    input_text = request.form['input_text']
    inputs = tokenizer.encode("paraphrase: " + input_text, return_tensors="pt")
    outputs = model.generate(inputs, max_length=1000, do_sample=True, num_return_sequences=2)
    paraphrases = [tokenizer.decode(output, skip_special_tokens=True) for output in outputs]
    return render_template('index.html', input_text=input_text, paraphrases=paraphrases)

if __name__ == '__main__':
    parrot.run(debug=True)