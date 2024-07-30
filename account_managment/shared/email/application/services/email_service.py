from account_managment.shared.email.domain import (EmailSender)


class EmailManagerService:

    def __init__(self, email_service: EmailSender):
        self.email_service = email_service

    def send_email(self):
        return self.email_service.send_email()
