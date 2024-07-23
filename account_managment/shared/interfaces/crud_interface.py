from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from sqlmodel import SQLModel

Model = TypeVar("Model", bound=SQLModel)


class ICrud(ABC, Generic[Model]):
    @abstractmethod
    def insert(self, user_create: Model) -> bool:
        pass

    @abstractmethod
    def get_one(self, email: str) -> Model | None:
        pass
