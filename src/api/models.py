from typing import NamedTuple  # typed named tuple

class OTP_Params(NamedTuple):
    """
    Modifiable params: `phone`, `otp_code`
    
    Default params: `api_key`, `secret_key`, `brand_name`, `sms_type`
    """

    phone: str
    otp_code: str
    api_key: str = "FC3105030010CFA43486E8487C94BA"
    secret_key: str = "CCFE6EDD25DC8711DB78E4BFE704F0"
    brand_name: str = "BaoTriXeMay"
    # 1 means that message will be sent using a hotline number;
    # 2 means that message will be sent using brand name
    sms_type: int = 2