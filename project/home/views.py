from flask import flash, redirect, session, url_for, render_template, Blueprint, request, url_for
from project import app, db
from project.models import ClientPosts, UserMessages
from flask_login import login_required
from flask_mail import Mail, Message
from .forms import ContactForm
from datetime import datetime, timedelta
from functools import wraps

home_blueprint = Blueprint(
    'home', __name__,
    template_folder="templates"
)

# create the mail object
mail = Mail(app)

@home_blueprint.route("/")
def home():
    return render_template("index.html")


@home_blueprint.route("/contact", methods=["POST", "GET"])
def contact():
	try:
		error = None
		contact_form = ContactForm()

		if request.method =='POST' and contact_form.validate_on_submit():
			user_name = contact_form.name.data
			user_email = contact_form.email.data
			user_phone = contact_form.phone.data
			user_msg = contact_form.msg_body.data
			current_dt = datetime.now()
			date_sent = current_dt.strftime("%Y-%m-%d %H:%M:%S")

			subject = "New Message from " + user_name + " via MasterlyWriters.com"

			new_msg = UserMessages(
				sender_name=user_name,
				sender_email=user_email,
				sender_phone=user_phone,
				message_details=user_msg,
				date_sent=date_sent,
				msg_read=False
			)

			db.session.add(new_msg)
			db.session.commit()

			msg = Message(subject,
				sender=user_email,
				recipients=['sindani254@gmail.com', 'masterlyprowriters@gmail.com'])
			msg.body = user_msg
			mail.send(msg)

			flash('Thank you!! Your message was sent successfully.')
			return redirect(url_for('home.contact'))

		return render_template("contact.html", contact_form=contact_form)
	except Exception as e:
		return (str(e))


@home_blueprint.route("/pricing")
def pricing():
	return render_template("pricing.html")


@home_blueprint.route("/how_it_works")
def how_it_works():
	return render_template("how_it_works.html")


@home_blueprint.route("/services")
def services():
	return render_template("services.html")
