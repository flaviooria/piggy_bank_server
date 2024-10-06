from typing import Tuple

from pydantic import BaseModel, EmailStr

from account_managment.shared.email.application.services.email_bases import (
    HtmlEmailTemplateService,
)
from account_managment.shared.email.application.services.smtp_email_services import (
    SmtpEmailService,
)

smtp_service = SmtpEmailService(mail_from=("no reply", "noreply@piggy-bank.com"))


async def send_notification_email(
    *,
    to: Tuple[str, EmailStr] | str | None,
    subject: str | None,
    template: HtmlEmailTemplateService,
    data: dict | BaseModel | str
):
    await smtp_service.subject(subject).to(to).build_template(template).create_email_sender(data).send_email()
