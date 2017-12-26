from model.case import Case


class AbnormalCase(Case):
    def __init__(self, date, status, receipt_number, cause):
        super().__init__(date, status, receipt_number, 'abnormal')
        self.cause = cause