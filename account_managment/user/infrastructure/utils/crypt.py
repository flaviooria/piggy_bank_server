from bcrypt import checkpw, gensalt, hashpw


class Crypt:
    @staticmethod
    def _str_to_bytes(text: str) -> bytes:
        return text.encode()

    @staticmethod
    async def encrypt(password: str) -> str:
        return hashpw(Crypt._str_to_bytes(password), gensalt()).decode()

    @staticmethod
    async def verify(password_plain: str, password_hashed: str) -> bool:
        return checkpw(Crypt._str_to_bytes(password_plain), Crypt._str_to_bytes(password_hashed))
