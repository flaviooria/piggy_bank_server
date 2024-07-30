import os
from pathlib import Path

from jinja2 import Environment, FileSystemLoader
from pydantic import BaseModel

from account_managment.shared.email.domain import EmailSender


class EmailBase:

    def __init__(self):
        pass

    def build_template(self, html_template: "HtmlEmailTemplateService"):
        pass

    def create_email_sender(self, data: dict | BaseModel | str) -> EmailSender:
        pass


class HtmlEmailTemplateService:
    """
    Class to read and render the html templates for each mail type in each use case.
    """

    def __init__(self, template: str, path_template: str | None = "."):
        """
        Initializes an instance of the HtmlEmailService class.

        Args:
            template (str): The name of the HTML template file.
            path_template (str | None, optional): The path to the
            directory containing the HTML template file. Defaults to ".".

        Returns:
            None
        """
        environment = Environment(loader=FileSystemLoader(path_template))

        if path_template != ".":
            path_template = self.__found_template(path_template)

            environment = Environment(loader=FileSystemLoader(path_template))

        # Read the template file
        self._template = environment.get_template(template)

    @classmethod
    def __found_template(cls, template_file: str):
        grandfather_dir = Path(os.path.dirname(__file__)).parent.parent  # => account_managment\shared\email
        template_dir = os.path.join(grandfather_dir, template_file)

        if Path(template_dir).exists():
            return Path(template_dir)

        raise FileNotFoundError(f"{template_dir} not exists")

    def render(self, data: dict | BaseModel):
        """
        Renders an HTML email template with the given data.

        Args:
            data (dict | BaseModel): The data to be used for rendering the template.
                If the data is an instance of BaseModel, its model_dump() method will be called.

        Returns:
            str: The rendered HTML email template.
        """

        _data = data

        if not isinstance(data, dict):
            _data = data.model_dump()

        return self._template.render(_data)
