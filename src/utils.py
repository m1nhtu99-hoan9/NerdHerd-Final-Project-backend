# expose authentication utility functions
from ._auth_ import check_password, hash_password, encode_token, decode_token

from base64 import b64decode, b64encode


def btoa(base_str: str) -> str:
    """ Convert a string to it base-64 form """
    ascii_bytes = base_str.encode("ascii")
    base64_bytes = b64encode(ascii_bytes)
    return base64_bytes.decode("ascii")


def atob(byted_str: str) -> str:
    """ Convert a base-64 encrypted string to decrypted form """
    base64_bytes = byted_str.encode("ascii")
    ascii_bytes = b64decode(base64_bytes)
    return ascii_bytes.decode("ascii")
