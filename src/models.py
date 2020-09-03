import bcrypt

class User(UserMixin): 
  phone_num: str
  password: str

user = User()
print(dir(user))
print(vars(user))

hashed = bcrypt.hashpw(password=b"secret password", salt=bcrypt.gensalt())

print(bcrypt.checkpw(b"secret password", hashed))
