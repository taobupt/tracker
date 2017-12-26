from model.case import Case


class ReceivedCase(Case):
    def __init__(self, date, status, receipt_number, form_type):
        super().__init__(date, status, receipt_number, 'received')
        self.form_type = form_type
