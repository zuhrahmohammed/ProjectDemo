from flask import Flask, render_template, request
from similarity_model import compare_to_ontology_instances

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    message = request.form.get("message", "")
    score = compare_to_ontology_instances(message)
    return render_template('index.html', score=round(score, 4), message=message)

if __name__ == '__main__':
    app.run(debug=False)
