import asyncio

from pydantic import BaseModel

from account_managment.shared.email.application import (
    HtmlEmailTemplateService,
    SmtpEmailService,
)
from account_managment.shared.email.domain import SmtpOptions


class RegisterTemplate(BaseModel):
    username: str


async def main():
    register_email_template = HtmlEmailTemplateService(template="register.mjml")

    # Envio de mensaje de email, con plantilla, las credenciales las lee de las variable de entorno
    smtp_service = SmtpEmailService(
        to=("Flavio", "flavio.oriap@gmail.com"),
        subject="Registro1 ",
        mail_from=("no reply", "noreply_test1@gmail.com"),
    )

    response = (
        await smtp_service.build_template(register_email_template)
        .create_email_sender({"username": "Flavio"})
        .send_email()
    )

    print("status email => ", response)

    # Envio de email con smtp como base model
    smtp_opts = SmtpOptions(
        host="smtp.ethereal.email",
        port=587,
        user="natalie24@ethereal.email",
        password="qhWmvemsKTzyCkgZdE",
        tls=True,
    )

    smtp_service2 = SmtpEmailService(
        to=("Flavio", "flavio.oriap@gmail.com"),
        subject="Registro2",
        mail_from=("no reply", "noreply_test2@gmail.com"),
    )
    smtp_service2.set_credentials(smtp=smtp_opts)

    response2 = (
        await smtp_service2.build_template(register_email_template)
        .create_email_sender({"username": "Prueba 2"})
        .send_email()
    )

    print("status email => ", response2)

    # Envio de email sin template
    smtp_service3 = SmtpEmailService(
        to=("Flavio", "flavio.oriap@gmail.com"),
        subject="Registro3",
        mail_from=("no reply", "noreply_test3@gmail.com"),
    )

    smtp_service3.set_credentials(
        host="smtp.ethereal.email",
        port=587,
        user="natalie24@ethereal.email",
        password="qhWmvemsKTzyCkgZdE",
        tls=True,
    )

    response3 = await smtp_service3.create_email_sender("Hola esto es un email de prueba").send_email()

    print("status email => ", response3)


if __name__ == "__main__":
    asyncio.run(main())
