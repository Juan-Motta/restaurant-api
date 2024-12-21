import base64
import binascii
import hashlib
import secrets
import string


class PasswordManager:
    """
    A utility class for generating and managing secure passwords.

    This class provides methods for generating random strings, creating
    secure password hashes using PBKDF2 with SHA-256 and complatible with
    Django, and verifying passwords against stored hashes. The hashing
    process includes a salt and iteration count to adhere to best security
    practices.

    Methods:
    --------
    get_random_string(length: int = 12, allowed_chars: str = string.ascii_letters + string.digits) -> str:
        Generates a random string of the specified length using allowed characters.

    generate_password(password: str, encoding: str = "utf-8", errors: str = "strict", iterations: int = 30000) -> str:
        Generates a secure password hash from the provided plaintext password.

    hash_pbkdf2_sha256(password: str, encoding: str, iterations: int, errors: str) -> str:
        Produces a PBKDF2 SHA-256 hash of a password and returns a formatted string.

    verify_password(stored_password: str, provided_password: str) -> bool:
        Checks if the provided password matches the stored password hash.
    """

    @classmethod
    def get_random_string(
        cls,
        length: int = 12,
        allowed_chars: str = string.ascii_letters + string.digits,
    ) -> str:
        """
        Generates a random string of the specified length using allowed characters.

        Parameters:
        ----------
        length : int
            The length of the generated random string (default is 12).

        allowed_chars : str
            The characters allowed in the generated random string
            (default includes both uppercase, lowercase letters and digits).

        Returns:
        -------
        str
            A random string composed of the specified allowed characters.
        """
        return "".join(secrets.choice(allowed_chars) for i in range(length))

    @classmethod
    def generate_password(
        cls,
        password: str,
        encoding: str = "utf-8",
        errors: str = "strict",
        iterations: int = 30000,
    ) -> str:
        """
        Generates a secure password hash from the provided plaintext password
        using PBKDF2 with SHA-256.

        Parameters:
        ----------
        password : str
            The plaintext password to be hashed.

        encoding : str
            The character encoding for the password (default is "utf-8").

        errors : str
            The error handling scheme for encoding (default is "strict").

        iterations : int
            The number of iterations for the PBKDF2 hashing process
            (default is 30,000).

        Returns:
        -------
        str
            A formatted string containing the hash, salt, and iteration count
            of the password.
        """
        return cls.hash_pbkdf2_sha256(
            password=password, encoding=encoding, errors=errors, iterations=iterations
        )

    @classmethod
    def hash_pbkdf2_sha256(
        cls, password: str, encoding: str, iterations: int, errors: str
    ) -> str:
        """
        Produces a PBKDF2 SHA-256 hash of a password, including a salt
        and iteration count.

        Parameters:
        ----------
        password : str
            The plaintext password to hash.

        encoding : str
            The character encoding for the password (must match the format).

        iterations : int
            The number of iterations for the PBKDF2 hashing process.

        errors : str
            The error handling scheme for encoding.

        Returns:
        -------
        str
            A formatted string representing the hashing algorithm, iteration
            count, salt, and the resultant hash.
        """
        password = password.encode(encoding, errors)
        salt = cls.get_random_string()
        salt_byte = salt.encode(encoding, errors)
        _hash = hashlib.pbkdf2_hmac("sha256", password, salt_byte, iterations, None)
        _hash = base64.b64encode(_hash).decode("ascii").strip()
        password = "%s$%d$%s$%s" % ("pbkdf2_sha256", iterations, salt, _hash)
        return password

    @classmethod
    def verify_password(cls, stored_password: str, provided_password: str):
        """
        Verifies the provided password against a stored password hash.

        Parameters:
        ----------
        stored_password : str
            The previously hashed password string that contains the hashing
            algorithm, iteration count, salt, and hash.

        provided_password : str
            The plaintext password to verify against the stored password.

        Returns:
        -------
        bool
            True if the provided password matches the stored password,
            False otherwise.
        """
        [*_, interations, salt, _hash] = stored_password.split("$")
        pwdhash = hashlib.pbkdf2_hmac(
            "sha256",
            provided_password.encode("utf-8"),
            salt.encode("utf-8"),
            int(interations),
        )
        if pwdhash == binascii.a2b_base64(_hash):
            return True
        return False
