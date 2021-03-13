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

    # JWT
    JWT_SECRET_KEY = '@df34FD%d^$W#%s#dsY$'
    JWT_TOKEN_LOCATION = ['cookies']
    JWT_ACCESS_COOKIE_PATH = '/'
    JWT_REFRESH_COOKIE_PATH = '/'
    JWT_COOKIE_CSRF_PROTECT = True
    JWT_COOKIE_SECURE = False

class ProductionConfig(Config):
    pass


class DevelopmentConfig(Config):
    DEBUG = True
