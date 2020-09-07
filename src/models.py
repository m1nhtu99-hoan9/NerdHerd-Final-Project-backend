from enum import Enum
from datetime import datetime
from typing import NamedTuple  # typed named tuple

# enumeration member names are seperated by space character
# @reference https://docs.python.org/3/library/enum.html#functional-api
USER_ROLES = Enum("USER_ROLES", "Staff")

class User(NamedTuple):
    full_name: str
    phone: str
    password: str
    role: USER_ROLES
    license_key: str

class Bank(NamedTuple):
    bank_id: str
    bank_name: str
    license_key: str
    branch: str
    branch_id: str
    staff_list: str
    expired_date: datetime

class Customer(NamedTuple): 
    phone: str,
    credit_score: float