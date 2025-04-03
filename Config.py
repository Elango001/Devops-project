from urllib.parse import quote

password = "__Elango@2006"  #MySQL password
encoded_password = quote(password)
#if your password contain "@" symbol then we hafta use qoute()

class config:
    SECRET_KEY = 'nothing'
    SQLALCHEMY_DATABASE_URI = f'mysql+pymysql://elango:{encoded_password}@localhost/user_registration'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
