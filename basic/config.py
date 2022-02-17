
class Config:

    ############ security CSRF ####################

    SECRET_KEY = 'secret'#string of our choose


    ############ set up database location #####################
    #sqlite help us to have database as a file in our location
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    #SMTP configuration
    MAIL_SERVER = "smtp-mail.outlook.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "hoda_sanij@outlook.com"
    MAIL_PASSWORD = "Mylittledog1234$"
