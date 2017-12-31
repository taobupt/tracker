from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
from model.mailed_case import MailedCase
from model.produced_case import ProducedCase
from model.received_case import ReceivedCase
from model.abnormal_case import AbnormalCase
from model.invalid_case import InvalidCase
import constants
from flask_celery import make_celery
from celery.result import AsyncResult
import json
import redis

app = Flask(__name__)
app.config['CELERY_RESULT_BACKEND'] = constants.CELERY_RESULT_BACKEND
app.config['CELERY_BROKER_URL'] = constants.CELERY_BROKER_URL

celery = make_celery(app)


def save_file(self, content):
    with open(self.file_name, 'w')as f:
        f.write(content)


def add_one(num):
    ind = 0
    while ind < len(num):
        if num[ind].isdigit():
            break
        else:
            ind += 1
    return num[0:ind] + str(int(num[ind:]) + 1)

@app.route('/')
def hello_world():
    return render_template('index.html')


@app.route('/query')
def get_case():
    with app.app_context():
        start = request.args.get('receipt_number')
        case_num = int(request.args.get('case_number'))
        tasks = []
        for i in range(case_num):
            tasks.append(query.delay(start).id)
            start = add_one(start)
        save.delay([], tasks)
        return "querying......"

@celery.task(name = 'tracker.save')
def save(results, tasks):
    completed_tasks = []
    for task in tasks:
        if AsyncResult(task).ready():
            completed_tasks.append(task)
            results.append(task)
    tasks = list(set(tasks) - set(completed_tasks))
    if len(tasks) > 0:
        save.apply_async((results, tasks), countdown=1)
    else:
        r = redis.StrictRedis(host='localhost', port=6379, db=0)
        with open('./static/data/data.json','w')as f:
            f.write(json.dumps([json.loads(r.get("celery-task-meta-"+x))["result"] for x in results]))
            #f.write('\n'.join(results))


@celery.task(name = 'tracker.query',serializer="json")
def query(num):
    constants.data[3] = ('appReceiptNum', num)
    response = requests.post('https://egov.uscis.gov/casestatus/mycasestatus.do', headers=constants.headers,
                             cookies=constants.cookies,
                             data=constants.data).text
    soup = BeautifulSoup(response, 'html.parser')
    core = soup.find_all('div', {'class': 'rows text-center'})
    case_model = None
    for date in core:
        current_status = date.find('h1').text
        text = date.find('p').text.split(',')
        start_date = ' '.join(''.join(xx for xx in text[:2]).split(' ')[1:])
        if current_status == 'Card Was Mailed To Me':
            request_date = ' '.join(''.join(xx for xx in text[3:5]).split(' ')[-3:])
            case_model = MailedCase(start_date, current_status, num, request_date)
        elif current_status == 'Case Was Received':
            form_type = text[2].split(' ')[-1]
            case_model = ReceivedCase(start_date, current_status, num, form_type)
        elif current_status == 'New Card Is Being Produced':
            case_model = ProducedCase(start_date, current_status, num)
        elif len(current_status) == 0:
            case_model = InvalidCase(None, None, num)
        else:
            case_model = AbnormalCase(start_date, current_status, num, text[2])
    return case_model.__dict__

if __name__ == '__main__':
    app.run(debug=True)
