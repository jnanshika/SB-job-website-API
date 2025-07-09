import os

class Config:
    JWT_SECRET_KEY = "eZgaF9ESATNIyshm78i9"
    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:root@localhost:3306/jobconnect"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = "developement"
    #for email
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 465
    SMTP_USERNAME = ''  #gmailid
    SMTP_PASSWORD = ''  #app password
    MAIL_SENDER = 'noreply@gamil.com'