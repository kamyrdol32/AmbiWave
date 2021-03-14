class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = "DFGs34fdvgss#$dsfd%EF#3245SD%#%E^%$^&$#S@#TY#Y&"

    SESSION_COOKIE_SECURE = False

    # MYSQL
    MYSQL_DATABASE_USER = "pi"
    MYSQL_DATABASE_PASSWORD = "Ev12321"
    MYSQL_DATABASE_DB = "AmbiWave"
    MYSQL_DATABASE_HOST = "evgaming.duckdns.org"

    # MAIL
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USERNAME = "kamyrdol32test@gmail.com"
    MAIL_PASSWORD = "iqvfqchwmxycqdbk"
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
