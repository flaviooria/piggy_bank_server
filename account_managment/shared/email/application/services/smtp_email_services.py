from typing import Tuple, overload

import emails
from pydantic import BaseModel, EmailStr
from typing_extensions import Self

from account_managment.common import settings
from account_managment.shared.email.application.services.email_bases import (
    EmailBase,
    HtmlEmailTemplateService,
)
from account_managment.shared.email.domain.interfaces.email_sender import EmailSender
from account_managment.shared.email.domain.models.email_models import SmtpOptions


def strtobool(value: str | bool) -> bool:
    if isinstance(value, bool):
        return value

    if value.lower() in ("yes", "true", "t", "1"):
        return True
    elif value.lower() in ("no", "false", "f", "0"):
        return False
    else:
        raise ValueError(f"{value} is not a valid boolean value, [yes, true, t, 1, no, false, f, 0].")


class SmtpEmail(EmailSender):
    def __init__(self, details: dict, msg: str):
        self._details = details
        self._msg = msg

    async def send_email(self) -> bool:
        try:
            subject = self._details.pop("subject")
            to = self._details.pop("to")
            _from = self._details.pop("mail_from")
            smtp = self._details.pop("smtp")

            if subject is None:
                raise Exception("subject is required")

            if to is None:
                raise Exception("to is required")

            if _from is None:
                raise Exception("mail_from is required")

            _smtp = SmtpOptions.model_validate(smtp)

            response = emails.html(html=self._msg, subject=subject, mail_from=_from).send(
                to=to, smtp=_smtp.model_dump()
            )

            email = to[1] if isinstance(to, Tuple) else to

            if response.success:
                print(f"Message sent to {email}")
            else:
                print(f"Message could not be sent to: {email}")
            return response.success
        except Exception as e:
            raise e


class SmtpEmailService(EmailBase):
    """
    Class to send emails using smtp protocol
    """

    def __init__(
        self,
        to: Tuple[str, EmailStr] | str | None = None,
        mail_from: Tuple[str, EmailStr] | str | None = None,
        subject: str | None = None,
    ):
        """
        Initializes an instance of the class with the provided parameters.

        Args:
            to (Tuple[str, EmailStr] | str): The recipient(s) of the email. It can be a tuple of (name, email) or a
            single email address.
            mail_from (Tuple[str, EmailStr] | str): The sender of the email. It can be a tuple of (name, email) or a
            single email address.
            subject (str): The subject of the email.

        Returns:
            None

        Examples:
            .. code-block:: python
                register_email_template = HtmlEmailTemplateService(
        template="register.mjml")

                # Envio de mensaje de email, con plantilla, las credenciales las lee de las variable de entorno
                smtp_service = SmtpEmailService(to=("Flavio", 'flavio.oriap@gmail.com'), subject="Registro1 ",
                                                mail_from=("no reply", "noreply_test1@gmail.com"))

                response = await smtp_service.build_template(register_email_template).create_email_sender(
                    {"username": "Flavio"}).send_email()

                print("status email => ", response)

                # Envio de email con smtp como base model
                smtp_opts = SmtpOptions(host="smtp.ethereal.email", port=587, user="natalie24@ethereal.email",
                                        password="qhWmvemsKTzyCkgZdE", tls=True)

                smtp_service2 = SmtpEmailService(to=("Flavio", 'flavio.oriap@gmail.com'), subject="Registro2",
                                                mail_from=("no reply", "noreply_test2@gmail.com"))
                smtp_service2.set_credentials(smtp=smtp_opts)

                response2 = await smtp_service2.build_template(register_email_template).create_email_sender(
                    {"username": "Prueba 2"}).send_email()

                print("status email => ", response2)

                # Envio de email sin template
                smtp_service3 = SmtpEmailService(to=("Flavio", 'flavio.oriap@gmail.com'), subject="Registro3",
                                                mail_from=("no reply", "noreply_test3@gmail.com"))

                smtp_service3.set_credentials(host="smtp.ethereal.email", port=587, user="natalie24@ethereal.email",
                                            password="qhWmvemsKTzyCkgZdE", tls=True)

                response3 = await smtp_service3.create_email_sender(
                    "Hola esto es un email de prueba").send_email()

                print("status email => ", response3)

        Raises:
            None
        """

        super().__init__()

        self._params = {
            "to": to,
            "mail_from": mail_from,
            "subject": subject,
        }

        self._html_template: HtmlEmailTemplateService | None = None
        self.set_credentials_from_env()

    def set_credentials_from_env(self):
        self._params["smtp"] = {
            "host": settings.SMTP_HOST,
            "port": int(settings.SMTP_PORT),
            "user": settings.SMTP_USER,
            "password": settings.SMTP_PASSWORD,
            "ssl": strtobool(settings.SMTP_SSL),
            "tls": strtobool(settings.SMTP_TLS),
        }

    def subject(self, subject: str):
        self._params["subject"] = subject
        return self

    def mail_from(self, mail_from: Tuple[str, EmailStr] | str):
        self._params["mail_from"] = mail_from
        return self

    def to(self, to: Tuple[str, EmailStr] | str):
        self._params["to"] = to
        return self

    @overload
    def set_credentials(
        self,
        *,
        host: str,
        port: int,
        user: str,
        password: str,
        ssl: bool = False,
        tls: bool = False,
    ):
        """
        Set the credentials for the SMTP server.

        Args:
            host (str): The hostname or IP address of the SMTP server.
            port (int): The port number of the SMTP server.
            user (str): The username for authentication.
            password (str): The password for authentication.
            ssl (bool, optional): Whether to use SSL/TLS encryption. Defaults to False.
            tls (bool, optional): Whether to use SSL/TLS encryption. Defaults to False.

        Example:
            .. code-block:: python
                from account_managment.shared.email.application.services import SmtpEmailService

                smtp_service = SmtpEmailService(
                    to=("Jhon Doe", 'jdoe@gmail.com'),
                    subject="Register",
                    mail_from=("no reply", "another@gmail.com")
                )


                smtp_service.set_credentials(
                    host="host@example.com",
                    port=587,
                    user="username",
                    password="xxxxxxxxxx"
                )

        Returns:
            None
        """

        pass

    @overload
    def set_credentials(self, smtp: dict | SmtpOptions):
        """
        Set the credentials for the SMTP server.

        Args:
            smtp (dict | SmtpOptions): The SMTP credentials as a dictionary or an instance of the SmtpOptions class.
                - dict: A dictionary with the following keys:
                    - host (str): The SMTP server host.
                    - port (int): The SMTP server port.
                    - username (str): The username for authentication.
                    - password (str): The password for authentication.
                    - ssl (bool, optional): Whether to use SSL/TLS encryption. Defaults to False.
                    - tls (bool, optional): Whether to use SSL/TLS encryption. Defaults to False.
                - SmtpOptions: An instance of the SmtpOptions class with the following attributes:
                    - host (str): The SMTP server host.
                    - port (int): The SMTP server port.
                    - username (str): The username for authentication.
                    - password (str): The password for authentication.
                    - ssl (bool, optional): Whether to use SSL/TLS encryption. Defaults to False.
                    - tls (bool, optional): Whether to use SSL/TLS encryption. Defaults to False.

        Returns:
            None

        Examples:
            Set credentials using a dictionary:
            ```
            credentials = {
                'host': 'smtp.example.com',
                'port': 587,
                'username': 'user@example.com',
                'password': 'secret'
            }
            smtp_service.set_credentials(**credentials)

            # or

            smtp_service.set_credentials(smtp=credentials)
            ```

            Set credentials using an instance of SmtpOptions:
            ```
            from account_managment.shared.email.application.models.smtp_options import SmtpOptions

            smtp_options = SmtpOptions(
                host='smtp.example.com',
                port=587,
                username='user@example.com',
                password='secret'
            )

            smtp_service.set_credentials(smtp=smtp_options)

            # or

            smtp_service.set_credentials(**smtp_options.model_dump())
            ```
        """
        pass

    def set_credentials(self, **kwargs):
        smtp_kw = kwargs

        if "smtp" in kwargs:
            smtp = kwargs.get("smtp")

            if isinstance(smtp, SmtpOptions):
                smtp_kw = SmtpOptions.model_validate(smtp).model_dump()
            else:
                smtp_kw = smtp
        else:
            if "ssl" not in kwargs:
                kwargs["ssl"] = False

            if "tls" not in kwargs:
                kwargs["tls"] = False

        self._params["smtp"] = smtp_kw

    def build_template(self, html_template: HtmlEmailTemplateService) -> Self:
        """
        Sets the HTML email template for this instance of `SmtpEmailService`.

        Args:
            html_template (HtmlEmailTemplateService): The HTML email template to be set.

        Returns:
            SmtpEmailService: This instance of `SmtpEmailService` with the HTML email template set.
        """

        self._html_template = html_template

        return self

    def create_email_sender(self, data: dict | BaseModel | str) -> EmailSender:
        """
        Creates an instance of `EmailSender` based on the provided data.

        Args:
            data (dict | BaseModel | str): The data to be used for creating the `EmailSender`.
                If `data` is a dictionary or a `BaseModel`, it will be used to render the HTML email template.
                If `data` is a string, it will be used as the email message.

        Returns:
            EmailSender: An instance of `EmailSender` with the appropriate parameters.

        Raises:
            Exception: If `data` is a dictionary or a `BaseModel` and the `self._html_template` is `None`.

        """

        if self._html_template is None:
            if isinstance(data, BaseModel) or isinstance(data, dict):
                raise Exception("data must be a string")

            return SmtpEmail(self._params, data)

        _msg = self._html_template.render(data)

        self.reset()

        return SmtpEmail(self._params, _msg)

    def reset(self):
        self._html_template = None
