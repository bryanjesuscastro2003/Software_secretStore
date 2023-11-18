import random
import string
from cryptography.fernet import Fernet
import datetime
import jwt


def encrypt_text(key, text):
    # Create a Fernet object with the provided key
    fernet = Fernet(key)

    # Convert the text to bytes
    text_bytes = text.encode()

    # Encrypt the text
    encrypted_bytes = fernet.encrypt(text_bytes)

    # Convert the encrypted bytes to a string
    encrypted_text = encrypted_bytes.decode()

    return encrypted_text


def decrypt_text(key, encrypted_text):
    # Create a Fernet object with the provided key
    fernet = Fernet(key)

    # Convert the encrypted text to bytes
    encrypted_bytes = encrypted_text.encode()

    # Decrypt the text
    decrypted_bytes = fernet.decrypt(encrypted_bytes)

    # Convert the decrypted bytes to a string
    decrypted_text = decrypted_bytes.decode()

    return decrypted_text


def generate_random_text(size):
    # Generate a random text with the specified size
    random_text = ''.join(random.choices(string.ascii_letters + string.digits, k=size))

    return random_text


def generate_jwt(payload, secret, hours=5):
    # Add the 'exp' claim to the payload
    payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=hours)

    # Generate the JWT

    encoded_jwt = jwt.encode(payload, secret, algorithm='HS256')

    return encoded_jwt

def validate_jwt(encoded_jwt, secret):
    try:
        # Decode the JWT
        payload = jwt.decode(encoded_jwt, secret, algorithms=['HS256'])
        return True, payload
    except jwt.ExpiredSignatureError:
        return False, 'Token expired'
    except jwt.InvalidTokenError:
        return False, 'Invalid token'



