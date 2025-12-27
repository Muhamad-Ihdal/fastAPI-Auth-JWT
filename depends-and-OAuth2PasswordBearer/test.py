from db import create_table,add_user,get_user_by_email,get_user_by_id

# create_table()

user = get_user_by_email(email="ladie@gmail.com")
print(user)
