from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password:str) -> str:
    return pwd_context.hash(password)

def verify(inputan:str,pwd_asli:str) -> bool:
    return pwd_context.verify(inputan,pwd_asli)

create = hash_password(password="hello123")
print("===========================")
print(create)
print("===========================")
print("===========================")
print("===========================")

pwSalah = "halloworld"
pwBenar = "hello123"
print(verify(pwSalah,create))
print(verify(pwBenar,create))