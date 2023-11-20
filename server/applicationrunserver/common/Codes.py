import random
import string
from cryptography.fernet import Fernet
import datetime
import jwt


def encrypt_text(key, text):
    """
    Encrypts the provided text using the provided key.

    Args:
        key (bytes): The encryption key.
        text (str): The text to be encrypted.

    Returns:
        str: The encrypted text.
    """
    fernet = Fernet(key)
    text_bytes = text.encode()
    encrypted_bytes = fernet.encrypt(text_bytes)
    encrypted_text = encrypted_bytes.decode()
    return encrypted_text


def decrypt_text(key, encrypted_text):
    """
    Decrypts the provided encrypted text using the provided key.

    Args:
        key (bytes): The encryption key.
        encrypted_text (str): The text to be decrypted.

    Returns:
        str: The decrypted text.
    """
    try:
        fernet = Fernet(key)
        encrypted_bytes = encrypted_text.encode()
        decrypted_bytes = fernet.decrypt(encrypted_bytes)
        decrypted_text = decrypted_bytes.decode()
        return decrypted_text
    except Exception as e:
        return None



def generate_random_text(size):
    """
    Generates a random text with the specified size.

    Args:
        size (int): The size of the random text.

    Returns:
        str: The generated random text.
    """
    random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=size))
    return random_text


def generate_jwt(payload, secret, hours=5):
    """
    Generates a JWT (JSON Web Token) with the provided payload and secret.

    Args:
        payload (dict): The payload to be included in the JWT.
        secret (str): The secret key used to sign the JWT.
        hours (int, optional): The number of hours until the JWT expires. Defaults to 5.

    Returns:
        str: The generated JWT.
    """
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)
    encoded_jwt = jwt.encode(payload, secret, algorithm='HS256')
    return encoded_jwt


def validate_jwt(encoded_jwt, secret):
    """
    Validates the provided JWT using the provided secret.

    Args:
        encoded_jwt (str): The JWT to be validated.
        secret (str): The secret key used to sign the JWT.

    Returns:
        tuple: A tuple containing a boolean indicating whether the JWT is valid and the payload if valid, or an error message if invalid.
    """
    try:
        payload = jwt.decode(encoded_jwt, secret, algorithms=['HS256'])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, 'Token expired'
    except jwt.InvalidTokenError:
        return False, 'Invalid token'
    



