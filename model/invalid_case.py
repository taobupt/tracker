from model.case import Case


class InvalidCase(Case):
    def __init__(self, date, status, receipt_number):
        super().__init__(date, status, receipt_number, 'invalid')