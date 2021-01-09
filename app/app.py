import ast
from flask import Flask, render_template, jsonify, request
from handwritten_recognizer import k_point_rec
from data import template
from index import link


app = Flask(__name__)


@app.route('/compute', methods=['GET', 'POST'])
def compute():
    if request.method == 'POST':
        data = request.get_json()
        data = data['gesture']
        data = ast.literal_eval(data)
        letter = k_point_rec(data, template, 1000)
        return letter, 200


@app.route('/')
def index():
    return link


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
