import sys
from abc import abstractmethod
from pathlib import Path
from typing import ClassVar

from jinja2 import Environment, FileSystemLoader
from mjml import mjml_to_html
from pydantic import BaseModel

from account_managment.shared.email.domain import EmailSender


class EmailBase:

    def __init__(self):
        pass

    def build_template(self, html_template: "HtmlEmailTemplateService"):
        pass

    @abstractmethod
    def create_email_sender(self, data: dict | BaseModel | str) -> EmailSender:
        pass


class HtmlEmailTemplateService:
    """
    Class to read and render the html templates for each mail type in each use case.
    """

    TEMPLATE_FOLDER: ClassVar[str] = "shared/email/templates"

    def __init__(self, template: str, template_folder: str | None = TEMPLATE_FOLDER):
        """
        Initializes an instance of the HtmlEmailService class.

        Args:
            template (str): The name of the HTML template file.
            template_folder (str | None, optional): The path to the
            directory containing the HTML template file. Defaults to ".".

        Examples:

            .. code-block:: python
                from account_managment.shared.email.application.services import HtmlEmailTemplateService
                html_template = HtmlEmailTemplateService(template="register.jinja")
                html_template.render({"username": "Jhon Doe"})
                '<p>Hello, Jhon Doe</p>'

        Returns:
            None
        """

        template_folder_dir = self.__found_template_dir(template_folder)
        environment = Environment(loader=FileSystemLoader(template_folder_dir))

        if template_folder != HtmlEmailTemplateService.TEMPLATE_FOLDER:
            template_folder_dir = self.__found_template_dir(template_folder)

            environment = Environment(
                loader=FileSystemLoader(template_folder_dir))

        self._path_template = template_folder_dir.joinpath(template)

        if not self._path_template.exists():
            raise FileNotFoundError(f"{self._path_template} not exists")

        # Read the template file
        self._template = environment.get_template(template)

    @classmethod
    def __found_template_dir(cls, path_template: str | Path):
        PARENT_FOLDER = Path(sys.path[1])
        PROJECT_FOLDER = Path(PARENT_FOLDER / "account_managment")

        TEMPLATE_FOLDER = Path(PROJECT_FOLDER / path_template)

        if not TEMPLATE_FOLDER.exists():
            raise FileNotFoundError(f"{TEMPLATE_FOLDER} not exists")

        return TEMPLATE_FOLDER

    def render(self, data: dict | BaseModel):
        """
        Renders an HTML email template with the given data.

        Args:
            data (dict | BaseModel): The data to be used for rendering the template.
                If the data is an instance of BaseModel, its model_dump() method will be called.

        Returns:
            str: The rendered HTML email template.
        """

        _data_to_render = data

        if not isinstance(data, dict):
            _data_to_render = data.model_dump()

        if not str(self._path_template).endswith(".mjml"):
            return self._template.render(_data_to_render)

        rendered_mjml = self._template.render(data)
        return mjml_to_html(rendered_mjml).html
