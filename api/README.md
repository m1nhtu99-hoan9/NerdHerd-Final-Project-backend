# DOCUMENTATION

## `otp` Module

- `OTP_Params`: typed named tuple used as parameter for `send_otp_message` function mentioned below
- `get_otp_code`: Get random 6-digit OTP code
  - Params: None
  - Returns: `str`
- `send_otp_message`:
  - Params: 
    - `session: requests_futures.sessions.FutureSession` (a `FutureSession` instance)
    - `otp_params: __main__.OTP_Params` (a `OTP_Params` named tuple) 
  - Returns: 
    - `status_code: int` (HTTP response status code)
    - `resp_body: collection.namedtuple` (HTTP response body converted to an untyped named tuple)