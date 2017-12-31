CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_BROKER_URL = 'redis://localhost:6379'

cookies = {
    'JSESSIONID': 'DC794CCFC74359E21951DBC0D99944C9',
    '_ga': 'GA1.2.1900754108.1507668083',
    '_ceg.s': 'oy8i5d',
    '_ceg.u': 'oy8i5d',
    '_gid': 'GA1.3.705210248.1511805456',
}
headers = {
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
data = [
    ('changeLocale', ''),
    ('completedActionsCurrentPage', '0'),
    ('upcomingActionsCurrentPage', '0'),
    ('appReceiptNum', 'YSC1890000195'),
    ('caseStatusSearchBtn', 'CHECK STATUS'),
]