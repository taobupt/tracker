from model.case import Case


class MailedCase(Case):
    def __init__(self, date, status, receipt_number, request_date):
        super().__init__(date, status, receipt_number, 'mailed')
        self.request_date = request_date