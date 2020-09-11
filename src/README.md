# DOCUMENTATION

## Features

### OTP Confirmation

When user requests a search query on customer's credit score, a text message containing an OTP code is sent to the customer's phone. User needs to have this OTP in order to get access.

### Session management using JSON Web Token (JWT)

When user is logged in successfully, their login credential (user's phone number) is encrypted as an access token. When user sends request to protected routes, their access token need to be attached with its header. When user's token is expired or blacklisted, user need to re-login to be assigned with new token. Each access token is expired after 15 mins and is blacklisted after being expired.

### Password Encryption

This app uses `bcrypt` algorithm to produce encrypted password string. A raw password string can be hashed to multiple hashed strings, but a hashed string can only refer to one and only raw password string. Encrypted password produced by `bcrypt` algorithm can't be decrypted and can only be used to check if it matches user's input password.

For the purpose of demonstration, in this project:

- Raw password `aacc1234` is hashed and stored in database as `$2b$12$ULkwSWOtguo/0FdVnIUrUOqYx90BnmoYLd5nHEGe6EYfAfuMb1H8a`
- Raw password `aacc1235` is hashed and stored in database as `$2b$12$ULkwSWOtguo/0FdVnIUrUO1tXeb9r/8B9hE9/tZqQ9M6zGHn6.cr6`
- Raw password `aacc1236` is hashed and stored in database as `$2b$12$ULkwSWOtguo/0FdVnIUrUOu69DayvJ6AGWd1/OvJeB2eYVtnxbv/K`

## TODOs for the next versions

- Change `/otp` from public route to protected route
