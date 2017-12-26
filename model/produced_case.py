from model.case import Case


class ProducedCase(Case):
    def __init__(self, date, status, receipt_number):
        super().__init__(date, status, receipt_number, 'produced')