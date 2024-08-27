from account_managment.shared import ICrud
from account_managment.user.domain.models.user_model import Users


class IUser(ICrud[Users]):
    pass
