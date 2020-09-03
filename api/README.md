# DOCUMENTATION

## `otp` Module

- `OTP_Params`: Typed named tuple class of which instance used as parameter for `send_otp_message` function mentioned below
- `get_otp_code`: Get random 6-digit OTP code
  - Params: None
  - Returns: `str`
- `send_otp_message`: When called, send text message to user's phone number containing OTP code
  - Params: 
    - `session: requests_futures.sessions.FutureSession` (a `FutureSession` instance)
    - `phone_num: str` (customer's phone number) 
  - Returns: 
    - `status_code: int` (HTTP response status code)
    - `otp_code: str` (OTP number generated and sent to customer)
    - `resp_body: collection.namedtuple` (HTTP response body converted to an untyped named tuple)