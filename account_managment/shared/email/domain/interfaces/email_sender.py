from abc import ABC


class EmailSender(ABC):

    def send_email(self) -> bool:
        """
        Sends an email.

        Returns:
            bool: whether the email was sent successfully. otherwise False
        """
        pass
