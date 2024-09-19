from abc import ABC, abstractmethod


class EmailSender(ABC):
    @abstractmethod
    async def send_email(self) -> bool:
        """
        Sends an email.

        Returns:
            bool: whether the email was sent successfully. otherwise False
        """
        pass
