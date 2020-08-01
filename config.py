import os

class BaseConfig(object):
	DEBUG = False
	SECRET_KEY = '\x03\x19v\n\xc2\xfb\xe2\xea\xc9\x13\xefe\xb6Q\xad\xb5.D\xee\xbe\xf8\xed*\xb5'
	SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	# Flask-User settings
	USER_APP_NAME = "Masterly Writers for Academic Writing Services"
	USER_ENABLE_EMAIL = True
	USER_ENABLE_USERNAME = False
	USER_EMAIL_SENDER_NAME = "sindani254"
	USER_EMAIL_SENDER_EMAIL = "sindani254@gmail.com"
	#print(SQLALCHEMY_DATABASE_URI)


class TestConfig(BaseConfig):
	DEBUG = True
	TESTING = True
	WTF_CSRF_ENABLED = True
	SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory'
		

class DevConfig(BaseConfig):
	DEBUG = True
	WTF_CSRF_ENABLED = True


class ProductionConfig(BaseConfig):
	DEBUG = True
		