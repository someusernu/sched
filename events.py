import datetime


class Event:
    def __init__(self):
        now = datetime.datetime.now()
        self.submitted = now
        self.user_reminder = (datetime.datetime(year=now.year, month=now.month, day=now.day) +
                              datetime.timedelta(days=2))
        self.remind_before = True
        self.remind_in_day = True
        self.telegram_remind = True
        self.email_remind = True
        self.app_remind = True
        self.text = ''

    def set_telegram(self, value=True):
        self.telegram_remind = value

    def set_email(self, value=True):
        self.email_remind = value

    def set_app(self, value=True):
        self.app_remind = value

    def set_text(self, text):
        self.text = text

    def set_remind_before(self, value=True):
        self.remind_before = value

    def set_remind_in_day(self, value):
        self.remind_in_day = value

        