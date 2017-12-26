import requests
from bs4 import BeautifulSoup
from model.mailed_case import MailedCase
from model.produced_case import ProducedCase
from model.received_case import ReceivedCase
from model.abnormal_case import AbnormalCase


def add_one(num):
    ind = 0
    while ind < len(num):
        if num[ind].isdigit():
            break
        else:
            ind += 1
    return num[0:ind] + str(int(num[ind:]) + 1)


class Crawler:
    def __init__(self):
        self.file_name = 'case.html'
        self.cookies = {
            'JSESSIONID': 'DC794CCFC74359E21951DBC0D99944C9',
            '_ga': 'GA1.2.1900754108.1507668083',
            '_ceg.s': 'oy8i5d',
            '_ceg.u': 'oy8i5d',
            '_gid': 'GA1.3.705210248.1511805456',
        }
        self.headers = {
            'Origin': 'https://egov.uscis.gov',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/62.0.3202.94 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Cache-Control': 'max-age=0',
            'Referer': 'https://egov.uscis.gov/casestatus/mycasestatus.do',
            'Connection': 'keep-alive',
        }
        self.data = [
            ('changeLocale', ''),
            ('completedActionsCurrentPage', '0'),
            ('upcomingActionsCurrentPage', '0'),
            ('appReceiptNum', 'YSC1890000195'),
            ('caseStatusSearchBtn', 'CHECK STATUS'),
        ]

    def save_file(self, content):
        with open(self.file_name, 'w')as f:
            f.write(content)

    def query(self, num):
        self.data[3] = ('appReceiptNum', num)
        response = requests.post('https://egov.uscis.gov/casestatus/mycasestatus.do', headers=self.headers,
                                 cookies=self.cookies,
                                 data=self.data).text
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
            else:
                case_model = AbnormalCase(start_date, current_status, num, text[2])
        return case_model

    def query_range(self, start, num):
        cases = []
        for i in range(num):
            cases.append(self.query(start))
            start = add_one(start)
        return cases
