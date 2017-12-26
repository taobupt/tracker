from flask import Flask, render_template, request, jsonify
from crawler import Crawler
import json

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/query')
def query():
    craw = Crawler()
    case_number = int(request.args.get('case_number'))
    cases = craw.query_range(request.args.get('receipt_number'), case_number if case_number is not None else 1)
    cases = [json.dumps(case.__dict__) for case in cases]
    return jsonify(cases)


if __name__ == '__main__':
    app.run(debug=True)
