from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextField, PasswordField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers


class AdminLoginForm(FlaskForm):
    username = TextField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    login_submit = SubmitField('Sign In')


class AdminRegForm(FlaskForm):
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


class OrderForm(FlaskForm):	
	d_date = TextField('Due Date', validators=[DataRequired()])


class ClientToAdminMsgForm(FlaskForm):
    msg_details = TextAreaField(u'Type your message here', validators=[DataRequired(), Length(min=5, max=500)])
