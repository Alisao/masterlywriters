from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from flask_bootstrap import Bootstrap
from flask_dropzone import Dropzone
from flask_jsglue import JSGlue
from flask_mail import Mail, Message
import os

# create the application object
app = Flask(__name__)
Bootstrap(app)


bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.init_app(app)
jsglue = JSGlue()
jsglue.init_app(app)

# config
app.config.from_object(os.environ["APP_SETTINGS"])
print(os.environ["APP_SETTINGS"])

# create the sqlalchemy object
db = SQLAlchemy(app)

from project.users.views import users_blueprint
from project.admin.views import admin_blueprint
from project.home.views import home_blueprint

# register our blueprints
app.register_blueprint(users_blueprint)
app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint)

from project.models import User
login_manager.login_view = "users.session_new"
login_manager.login_message_category = 'info'

# create the dropzone object
dropzone = Dropzone(app)

# Dropzone settings
app.config['DROPZONE_UPLOAD_MULTIPLE'] = True
app.config['DROPZONE_ALLOWED_FILE_CUSTOM'] = True
app.config['DROPZONE_ALLOWED_FILE_TYPE'] = 'image/*, .pdf, .docx, .odt, .doc, application/msword,application/vnd.openxmlformats-officedocument.wordprocessingml.document, .zip, .rar, .7zip'

# Uploads settings
app.config['UPLOADED_FILES_DEST'] = os.getcwd() + '/static/file_uploads'
app.config['DROPZONE_MAX_FILE_SIZE'] = 30
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# configure flask mail
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_DEBUG'] = True
app.config['MAIL_USERNAME'] = 'sindani254@gmail.com'
app.config['MAIL_PASSWORD'] = 'Soen@30010010'
app.config['MAIL_DEFAULT_SENDER'] = None

app.config['MAIL_MAX_EMAILS'] = None
app.config['MAIL_SUPPRESS_SEND'] = False
app.config['MAIL_ASCII_ATTACHMENTS'] = False

# Flask-User settings
app.config['USER_APP_NAME'] = "Masterly Writers for Academic Writing Services"
app.config['USER_ENABLE_EMAIL'] = True
app.config['USER_ENABLE_USERNAME'] = False
app.config['USER_EMAIL_SENDER_NAME'] = "sindani254"
app.config['USER_EMAIL_SENDER_EMAIL'] = "sindani254@gmail.com"


# create the mail object
mail = Mail(app)


@login_manager.user_loader
def load_user(user_id):
	return User.query.filter(User.id == int(user_id)).first()
