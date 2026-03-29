import hmac
import hashlib

SECRET_KEY = b"super_secret_key"


def generate_signature(message):
    signature = hmac.new(
        SECRET_KEY,
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    return signature


def verify_signature(message, received_signature):

    expected_signature = hmac.new(
        SECRET_KEY,
        message.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(expected_signature, received_signature)