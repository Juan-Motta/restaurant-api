import string


class IPasswordManager:
    @classmethod
    def get_random_string(
        cls,
        length: int = 12,
        allowed_chars: str = string.ascii_letters + string.digits,
    ) -> str:
        raise NotImplementedError

    @classmethod
    def generate_password(
        cls,
        password: str,
        encoding: str = "utf-8",
        errors: str = "strict",
        iterations: int = 30000,
    ) -> str:
        raise NotImplementedError

    @classmethod
    def hash_pbkdf2_sha256(
        cls, password: str, encoding: str, iterations: int, errors: str
    ) -> str:
        raise NotImplementedError

    @classmethod
    def verify_password(cls, stored_password: str, provided_password: str):
        raise NotImplementedError
