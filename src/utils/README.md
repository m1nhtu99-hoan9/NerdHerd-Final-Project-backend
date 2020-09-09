# Documentation: Utilities

## Authentication Utilities

### Password Encryption

This app uses `bcrypt` algorithm to produce encrypted password string. A raw password string can be hashed to multiple hashed strings, but a hashed string can only refer to one and only raw password string. Encrypted password produced by `bcrypt` algorithm can't be decrypted and can only be used to check if it matches user's input password. 

For the purpose of demonstration, in this project:
- Raw password `aacc1234` is hashed and stored in database as `$2b$12$ULkwSWOtguo/0FdVnIUrUOqYx90BnmoYLd5nHEGe6EYfAfuMb1H8a`
- Raw password `aacc1235` is hashed and stored in database as `$2b$12$ULkwSWOtguo/0FdVnIUrUO1tXeb9r/8B9hE9/tZqQ9M6zGHn6.cr6`
- Raw password `aacc1236` is hashed and stored in database as `$2b$12$ULkwSWOtguo/0FdVnIUrUOu69DayvJ6AGWd1/OvJeB2eYVtnxbv/K`
