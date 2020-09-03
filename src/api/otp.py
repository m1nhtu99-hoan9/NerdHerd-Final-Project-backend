import os
import sys
import random
from requests_futures.sessions import FuturesSession

"""
    Add parent folder into system's list of path so that
    modules from `utils` folder can be accessed
"""
DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(DIR, "..")))

from models import OTP_Params
from utils.ds import json_loads_to_named_tuple

"""Notes
   - To convert a `named_tuple` to dictionary, do `named_tuple._asdict()`  
   - To get names of `named_tuple` fields, use `named_tuple._fields()`  
"""

def get_otp_code() -> str:
    """Get random 6-digit OTP code"""
    return "".join([random.choice("0123456789") for i in range(6)])


def send_otp_message(session: FuturesSession, phone_num: str):
    """Send an message with OTP code to user's phone number
    
    Parameters:
    - `session` (`requests_futures.sessions.FutureSession`): a `FutureSession` instance
    - `phone_num` (`str`): customer's phone number 
    
    Returns: 
    - status code (`int`),
    - otp code (`str`)
    - response body (untyped named tuple)
    """
    otp_code = get_otp_code()
    otp_params = OTP_Params(phone=phone_num, otp_code=otp_code)
    payload = {
        "Phone": otp_params.phone,
        "Content": f"Ma OTP cua ban la {otp_params.otp_code}",
        "ApiKey": otp_params.api_key,
        "SecretKey": otp_params.secret_key,
        "BrandName": otp_params.brand_name,
        "SmsType": otp_params.sms_type,
    }

    # future: concurrent.futures._base.Future
    future = session.get(
        "http://rest.esms.vn/MainService.svc/json/SendMultipleMessage_V4_get",
        params=payload,
    )
    # resp: requests.models.Response
    resp = future.result()

    # get result as an untyped named tuple
    resp_body = json_loads_to_named_tuple(resp.text, "OtpResponse")

    return resp.status_code, otp_code, resp_body


if __name__ == "__main__":
    """
    This section is for debugging purpose
    """

    # session = FuturesSession()
    # code, otp, data_body = send_otp_message(session, phone_num="0976162652")

    # print(f"Status code: {code}, of type {type(code)}")
    # print(f"OTP code is {otp}")
    # print(f"Data received: of type {type(data_body)}")
    # print(f"...content: {data_body}")
