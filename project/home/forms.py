from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import TextField, PasswordField, TextAreaField, StringField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
import phonenumbers


class ContactForm(FlaskForm):
    name = TextField(
        'name',
        validators=[DataRequired(), Length(min=3, max=25)]
    )
    email = TextField(
        'email',
        validators=[DataRequired(), Email(message="invalid email address"), Length(min=6, max=40)]
    )
    phone = StringField(
        'enter phone number',
        validators=[DataRequired(), Length(10)]
    )
    msg_body = TextAreaField(
        u'Your message', 
        validators=[DataRequired(), Length(min=5, max=10000)]
    )    

    def validate_phone(self, phone):
    	try:
    		p = phonenumbers.parse(phone.data)
    		if not phonenumbers.is_valid_number(p):
    			raise ValueError()
    	except (phonenumbers.phonenumberutil.NumberParseException, ValueError):
    		raise ValidationError("invalid phone number")
