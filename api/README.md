# DOCUMENTATION

## `otp` Module

- :page_with_curl: `OTP_Params`: Typed named tuple class modelling OTP request parameters 
- :punch: `get_otp_code`: Get random 6-digit OTP code
  - Params: None
  - Returns: `str`
- :key: :punch: `send_otp_message`: When called, send text message to user's phone number containing OTP code
  - Params: 
    - `session: requests_futures.sessions.FutureSession` (a `FutureSession` instance)
    - `phone_num: str` (customer's phone number) 
  - Returns: 
    - `status_code: int` (HTTP response status code)
    - `otp_code: str` (OTP number generated and sent to customer)
    - `resp_body: collection.namedtuple` (HTTP response body converted to an untyped named tuple)
