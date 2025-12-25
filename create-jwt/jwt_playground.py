from jose import jwt
from datetime import datetime, timedelta,timezone

SECRET_KEY = "INI_SECRET_RAHASI"
ALGORITHM = "HS256"

# data yang mau dimasukin ke token
payload = {
    "sub": "3",
    "email": "jhon@mail.com",
    "exp": datetime.now(timezone.utc) + timedelta(minutes=5)
}

# bikin token
token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

print("JWT TOKEN:")
print(token)

# decode token
decoded = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

print("\nDECODED PAYLOAD:")
print(decoded)
