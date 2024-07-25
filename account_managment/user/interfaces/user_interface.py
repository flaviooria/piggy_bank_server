# from abc import ABC, abstractmethod

from account_managment.shared import ICrud
from account_managment.user.models import Users


class IUser(ICrud[Users]):
    pass
