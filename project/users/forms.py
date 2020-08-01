from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextField, PasswordField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from project.models import User, ClientPosts, IPN, OrderAttachments, bcrypt, ClientMessages, WriterFiles
import phonenumbers


class LoginForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login_submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    name = TextField(
        'name',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    username = TextField(
        'username',
        validators=[DataRequired(), Length(min=4, max=25)]
    )
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message=None), Length(min=6, max=40)]
    )
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=8, max=25)]
    )
    confirm = PasswordField('retype password', validators=[DataRequired(), EqualTo('password', message='passwords must match')])
    phone = StringField('enter phone number', validators=[DataRequired(), Length(10)])
    reg_submit = SubmitField('Sign up')

    def validate_phone(self, phone):
    	try:
    		p = phonenumbers.parse(phone.data)
    		if not phonenumbers.is_valid_number(p):
    			raise ValueError()
    	except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
    		raise ValidationError("invalid phone number")


class ProfileForm(FlaskForm):
    name = TextField(
        'name',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    phone = StringField('enter phone number', validators=[DataRequired(), Length(10)])


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(
        'old password',
        validators=[DataRequired(), Length(min=8, max=25)]
    )
    new_password = PasswordField(
        'new password',
        validators=[DataRequired(), Length(min=8, max=25)]
    )
    confirm_new_pswd = PasswordField('retype password',
        validators=[DataRequired(),
        EqualTo('new_password',
        message='passwords must match')])


class OrderForm(FlaskForm):
    topic = TextField('Topic', validators=[DataRequired(), Length(min=5)])
    instructions = TextAreaField(u'Your Instructions', validators=[DataRequired(), Length(min=5, max=10000)])


class MessageForm(FlaskForm):
    msg_body = TextAreaField(u'Your message', validators=[DataRequired(), Length(min=5, max=10000)])


class RequestResetForm(FlaskForm):
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message="*invalid email address"), Length(min=6, max=40)]
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()

        if user is None:
            raise ValidationError('email address not found!')


class ResetPasswordForm(FlaskForm):
    password = PasswordField(
        'password',
        validators=[DataRequired(), Length(min=8, max=25)]
    )
    confirm_password = PasswordField('retype password', validators=[DataRequired(), EqualTo('password', message='passwords must match')])
