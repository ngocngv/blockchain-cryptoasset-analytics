class Config(object):

    SECRET_KEY = "secret"
    FLASK_ADMIN_SWATCH = 'cerulean'
    APP_NAME = "Blockchain and Cryptoasset Analytics"
    APP_SYSTEM_ERROR_SUBJECT_LINE = APP_NAME + " system error"

    CSRF_ENABLED = True

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    USER_APP_NAME = APP_NAME
    USER_ENABLE_CHANGE_PASSWORD = True
    USER_ENABLE_CHANGE_USERNAME = False
    USER_ENABLE_CONFIRM_EMAIL = True
    USER_ENABLE_FORGOT_PASSWORD = True
    USER_ENABLE_EMAIL = True
    USER_ENABLE_REGISTRATION = True 
    USER_REQUIRE_RETYPE_PASSWORD = True 
    USER_ENABLE_USERNAME = False 
    USER_ENABLE_REMEMBER_ME = True
    USER_REQUIRE_INVITATION = False

    USER_AFTER_LOGIN_ENDPOINT = 'main.afterlogin'
    USER_AFTER_LOGOUT_ENDPOINT = 'main.afterlogout'
    USER_AFTER_FORGOT_PASSWORD_ENDPOINT = 'user.login'

    BLOGGING_ENGLISH_FIRST = 1
    BLOGGING_POSTS_PER_PAGE = 10
    BLOGGING_PERMISSIONS = True
    BLOGGING_URL_PREFIX = "/blog"
    BLOGGING_KEYWORDS = ["blockchain", "cryptoassets", "analytics"]
    BLOGGING_ALLOW_FILEUPLOAD = True
    FILEUPLOAD_IMG_FOLDER = "fileupload"
    FILEUPLOAD_PREFIX = "/fileupload"
    FILEUPLOAD_ALLOWED_EXTENSIONS = ["png", "jpg", "jpeg", "gif"]
    
    ENV = ""

    SQLALCHEMY_DATABASE_URI = ''
    SQLALCHEMY_TRACK_MODIFICATIONS = False 

    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_SSL = False
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''
    MAIL_PASSWORD = ''
    MAIL_DEFAULT_SENDER  = ''

    USER_APP_NAME = 'Blockchain and Cryptoasset Analytics'
    USER_EMAIL_SENDER_NAME = 'Blockchain and Cryptoasset Analytics'
    USER_EMAIL_SENDER_EMAIL = ''

    ADMINS = [
        '"Blockchain and Cryptoasset Analytics" <blockchain.cryptoasset.analytics@gmail.com>',
        ]
