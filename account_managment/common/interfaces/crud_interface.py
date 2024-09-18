from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from pydantic import BaseModel
from tortoise import Model as TortoiseModel

AnyModel = TypeVar("AnyModel", BaseModel, TortoiseModel)


class ICrud(ABC, Generic[AnyModel]):
    @abstractmethod
    async def insert(self, model: AnyModel) -> AnyModel:
        pass

    @abstractmethod
    async def get_one(self, email: str) -> AnyModel | None:
        pass

    @abstractmethod
    async def get_all(self) -> list[AnyModel]:
        pass
