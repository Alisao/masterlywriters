from flask import flash, redirect, send_from_directory, session, render_template, request, url_for, Blueprint, jsonify
from flask_login import login_user, login_required, logout_user, current_user
from project import app, db
from .forms import LoginForm, RegisterForm, OrderForm, MessageForm
from project.models import User, ClientPosts, IPN, OrderAttachments, bcrypt, ClientMessages
import os
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, ALL, DATA, DEFAULTS, patch_request_class
from flask_dropzone import Dropzone
from sqlalchemy import inspect
from splinter import Browser
from selenium import webdriver
import random
import string
import sys
import urllib.parse
import requests

from werkzeug.datastructures import ImmutableOrderedMultiDict

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
FILE_DIR = '../static/file_uploads'
ERR_NO_FILE_SPECIFIED = 'error: no file specified'

VERIFY_URL_PROD = 'https://ipnpb.paypal.com/cgi-bin/webscr'
VERIFY_URL_TEST = 'https://ipnpb.sandbox.paypal.com/cgi-bin/webscr'

# Switch as appropriate
VERIFY_URL = VERIFY_URL_TEST

# CGI preamble
print('content-type: text/plain')
print()

users_blueprint = Blueprint(
    'users', __name__,
    template_folder='templates'
)

order_status = "pending_payment"
p_status = "pending_payment"
order_status_cancelled = "Cancelled"


media = UploadSet('media', default_dest=lambda app: app.instance_path)
configure_uploads(app, media)
patch_request_class(app)  # set maximum file size, default is 16MB



@users_blueprint.route("/new_session", methods=['GET', 'POST'])
def session_new():
    regform = RegisterForm()
    error = None
    loginform = LoginForm(request.form)

    return render_template('auth.html', regform=regform, error=error, loginform=loginform)


@users_blueprint.route("/login", methods=['GET', 'POST'])
def login():
    regform = RegisterForm()
    error = None
    loginerror = None
    loginform = LoginForm(request.form)
    if request.method == 'POST':
        if loginform.validate_on_submit():
            user = User.query.filter_by(
                username=loginform.username.data).first()
            if user is not None and bcrypt.check_password_hash(user.password, loginform.password.data):
                login_user(user, remember=True)
                if 'url' in session:
                    return redirect(session['url'])
                return redirect(url_for('home.home'))
            else:
                login_email = User.query.filter_by(
                    email=loginform.username.data).first()
                if login_email is not None and bcrypt.check_password_hash(login_email.password, loginform.password.data):
                    login_user(login_email)
                    if 'url' in session:
                        return redirect(session['url'])
                    return redirect(url_for('users.profile'))
                else:
                    loginerror = 'invalid credentials! please try again.'
        else:
            return "not validated"
    return render_template('auth.html', regform=regform, loginform=loginform, error=error, loginerror=loginerror)


@users_blueprint.route("/register", methods=['GET', 'POST'])
def register():
    regform = RegisterForm()
    error = None
    reg_uname_error = None
    reg_email_duplicate_error = None
    reg_phone_duplicate_error = None
    loginform = LoginForm(request.form)
    try:
        if regform.validate_on_submit():
            check_username = User.query.filter_by(
                username=regform.username.data).first()
            if check_username is not None:
                reg_uname_error = "*username already in use"
                error = "username already in use"

            check_email = User.query.filter_by(
                email=regform.email.data).first()
            if check_email is not None:
                reg_email_duplicate_error = "*email already in use"
                error = "email already in use"

            check_phone = User.query.filter_by(
                phone_number=regform.phone.data).first()
            if check_phone is not None:
                reg_phone_duplicate_error = "*phone number already in use"
                error = "phone number already in use"

            if error is None:
                user = User(
                    name=regform.name.data,
                    username=regform.username.data,
                    phone_number=regform.phone.data,
                    email=regform.email.data,
                    password=regform.password.data
                )
                db.session.add(user)
                db.session.commit()
                login_user(user)
                return redirect(url_for('users.profile'))

        return render_template(
            'auth.html',
            regform=regform,
            reg_uname_error=reg_uname_error,
            reg_email_duplicate_error=reg_email_duplicate_error,
            reg_phone_duplicate_error=reg_phone_duplicate_error,
            error=error, loginform=loginform)
    except Exception as e:
        return (str(e))


@users_blueprint.route('/place_order', methods=['GET', 'POST'])
def place_order():
    
    if current_user.is_authenticated:
        try:
            pending_orders = ClientPosts.query.filter_by(author_id=current_user.id, order_status="pending_payment").first()
            if pending_orders is not None:
                flash('Please complete payment for pending order to order again!')
                return redirect(url_for('users.profile'))
        except Exception as e:
            return (str(e))
        
        order_form = OrderForm(request.form)
        error = None
    else:
        session['url'] = url_for('users.place_order')
        return redirect(url_for('users.session_new'))
    return render_template('place_order.html', order_form=order_form, error=error)


@users_blueprint.route("/save_order", methods=['GET', 'POST'])
def save_order():
    order_form = OrderForm(request.form)
    error = None
    if request.method == 'POST' and order_form.validate_on_submit():
        d_date = datetime.now() + timedelta(hours=int(request.form['due_date']))
        new_order = ClientPosts(
            topic=order_form.topic.data,
            discipline=request.form['discipline'],
            paper_type=request.form['paper_type'],
            ac_level=request.form['ac_level'],
            total_pages=request.form['t_pages'],
            word_count=request.form['word_count'],
            spacing=request.form['spacing'],
            sources=request.form['sources'],
            due_date=d_date,
            paper_format=request.form['p_format'],
            instructions=order_form.instructions.data,
            order_status=order_status,
            payment_status=p_status,
            grand_total=request.form['g_total'],
            author_id=current_user.id
        )

        inspection = inspect(new_order)
        db.session.add(new_order)
        db.session.commit()

        new_order_id = new_order.id
        print(new_order_id)
        if "file_urls" in session:
            print('ziko')
            files_update = OrderAttachments.query.filter_by(file_db_save_status="pending").all()
            for file in files_update:
                file.file_db_save_status = "done"
                file.order_id = new_order_id
                db.session.commit()
                print("file details successfully updated")
        else:
            print('haziko')

        return redirect(url_for('users.profile'))
    return render_template('place_order.html', order_form=order_form, error=error)


@users_blueprint.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("home.home"))


@users_blueprint.route("/user_profile", methods=["GET", "POST"])
def profile():
    if not current_user.is_authenticated:
        session['url'] = url_for('users.profile')
        return redirect(url_for('users.session_new'))
    else:
        error = None

        # get all orders
        all_orders = get_client_order(current_user.id)
        posts_count = len(all_orders)

        
            
    return render_template(
        "profile.html", \
        error=error, \
        all_orders=all_orders, \
        posts_count=posts_count
    )


@users_blueprint.route("/view_order", methods=["GET", "POST"])
def view_order():
    error = None
    if not current_user.is_authenticated:
        session['url'] = url_for('users.profile')
        return redirect(url_for('users.session_new'))
    msg_form = MessageForm(request.form)

    order_sku = request.args.get('order_id')
    print(order_sku)
        
    recent_orders = ClientPosts.query.filter_by(id=order_sku).first()

    attachments = OrderAttachments.query.filter_by(order_id=order_sku).all()

    if "single_order_url" not in session:
            session['single_order_url'] = request.url        

    return render_template("single_order.html", error=error, recent_orders=recent_orders, attachments=attachments, msg_form=msg_form)


@users_blueprint.route("/cancel_order", methods=["GET", "POST"])
def cancel_order():
    order_id = request.args.get('order_id')
    current_order = ClientPosts.query.filter_by(id=order_id).first()
    current_order.order_status = "Cancelled"
    current_order.payment_status = "Cancelled"
    db.session.commit()
    return redirect(url_for('users.profile'))


@users_blueprint.route("/send_message", methods=["GET", "POST"])
def send_message():
    msg_form = MessageForm(request.form)
    error = None
    if request.method == 'POST' and msg_form.validate_on_submit():
        order_id = request.form['order_id_input']
        author_id = current_user.id
        msg_body = msg_form.msg_body.data

        currentDT = datetime.now()
        sentDT = currentDT.strftime("%Y-%m-%d %H:%M:%S")

        new_msg = ClientMessages(
            message_details=msg_body,
            date_sent=sentDT,
            order_id=order_id,
            author_id=author_id,
            msg_read=False
        )

        db.session.add(new_msg)
        db.session.commit()

        if "single_order_url" in session:
            return redirect(session['single_order_url'])
        else:
            return "ERROR: url NOT in session"


@users_blueprint.route("/reorder", methods=["GET", "POST"])
def reorder():
    return redirect(url_for('users.update_order'))


@users_blueprint.route("/purchase")
def purchase():
    if current_user.is_authenticated:
        try:
            user_id = current_user.id
            orders = get_client_order(user_id, order_status)
        except Exception as e:
            return(str(e))
    else:
        session['url'] = url_for('users.purchase')
        return redirect(url_for('users.session_new'))
    return render_template("purchase.html", user_id=get_current_user_id(), orders=orders)


@users_blueprint.route("/paypal_ipn", methods=["GET", "POST"])
def paypal_ipn_listener():

    print("IPN event received.")

    # Sending message as-is with the notify-validate request
    params = request.form.to_dict()
    params['cmd'] = '_notify-validate'
    headers = {'content-type': 'application/x-www-form-urlencoded',
               'user-agent': 'Masterly Writers PayPal Integration Test'}
    response = requests.post(VERIFY_URL, params=params,
                             headers=headers, verify=True)
    response.raise_for_status()

    # See if PayPal confirms the validity of the IPN received
    if response.text == 'VERIFIED':
        print("Verified IPN response received.")
        try:
            # Take action, e.g. update database to set user's
            payer_id = request.form.get('custom')
            gross_payment = request.form.get('payment_gross')
            p_status = request.form.get('payment_status')
            print(gross_payment)
            notifier_details = IPN(
                payer_id=payer_id,
                payer_email=request.form.get('payer_email'),
                payment_date=request.form.get('payment_date'),
                payer_first_name=request.form.get('first_name'),
                payer_last_name=request.form.get('last_name'),
                payment_gross=gross_payment,
                payment_fee=request.form.get('payment_fee'),
                payment_status=p_status,
                txn_id=request.form.get('txn_id')
            )
            db.session.add(notifier_details)
            db.session.commit()
            print("paypal ipn details successfully saved to the database")

            # update client's payment and order stata
            this_order = ClientPosts.query.filter_by(
                author_id=payer_id, order_status=order_status).first()
            this_order.order_status = "Writer pending"
            this_order.payment_status = p_status
            db.session.commit()
            print("order details successfully updated")

        except Exception as e:
            print(e)

    elif response.text == 'INVALID':
        # Don't trust
        print("Invalid IPN response.")
    else:
        print("Some other response.")
        print(response.text)
    return ""


@users_blueprint.route("/paypal_cancel")
def paypal_cancel():
    return render_template("paypal_cancel.html")


@users_blueprint.route("/paypal_success")
def paypal_success():
    try:
        return render_template("success.html")
    except Exception as e:
        return(str(e))


@users_blueprint.route("/update_order", methods=['GET', 'POST'])
def update_order():
    order_id = request.args.get('order_id')
    if current_user.is_authenticated:

        if "update_orders_url" not in session:
            session['update_orders_url'] = request.url

        order_form = OrderForm(request.form)
        error = None
        current_order = ClientPosts.query.filter_by(id=order_id).first()
        order_form.instructions.data = current_order.instructions

        spacing = current_order.spacing
        paper_format = current_order.paper_format

        # get files related to this order
        order_files = OrderAttachments.query.filter_by(order_id=order_id).all()

        
    else:
        session['url'] = url_for('users.place_order')
        return redirect(url_for('users.session_new'))

    return render_template("update_order.html", 
                    order_id=order_id,
                    current_order=current_order,
                    order_form=order_form,
                    spacing=spacing,
                    paper_format=paper_format,
                    order_files=order_files,
                    error=error)


@users_blueprint.route("/save_update", methods=['GET', 'POST'])
def save_update():

    try:
        order_form = OrderForm(request.form)
        order_id = request.form['order_id']
       
        sources = request.form['sources']
        due_date = datetime.now() + timedelta(hours=int(request.form['due_date']))
        instructions = order_form.instructions.data

        this_order = ClientPosts.query.filter_by(id=order_id).first()

        this_order.topic = order_form.topic.data
        this_order.discipline = request.form['discipline']
        this_order.paper_type = request.form['paper_type']
        this_order.ac_level = request.form['ac_level']
        this_order.total_pages = request.form['t_pages']
        this_order.word_count = request.form['word_count']

        this_order.spacing = request.form['spacing']
        this_order.paper_format = request.form['p_format']
        this_order.grand_total = request.form['g_total']
        db.session.commit()

        print("order successfully updated")

        if "file_urls" in session:
            print('ziko')
            files_update = OrderAttachments.query.filter_by(file_db_save_status="pending").all()
            for file in files_update:
                file.file_db_save_status = "done"
                file.order_id = order_id
                db.session.commit()
                print("file details successfully updated")
        else:
            print('haziko')

        return redirect(url_for('users.profile'))
    except Exception as e:
        return (str(e))


@users_blueprint.route('/upload_files', methods=['GET', 'POST'])        
def upload_files():
    target = os.path.join(APP_ROOT, '../static/file_uploads')
    order_form = OrderForm(request.form)
    error = None
    if "file_urls" not in session:
        session['file_urls'] = []
    # list to hold our uploaded image urls
    file_urls = session['file_urls']

    if request.method == 'POST':
        if not os.path.isdir(target):
            os.mkdir(target)

        for key, f in request.files.items():
            if key.startswith('file'):
                f_name = secure_filename(f.filename)
                f.save(os.path.join(target, f_name))

                # append file urls
                file_urls.append(f_name)
                session['file_urls'] = file_urls
                try:
                    upload_items = OrderAttachments(file_name=f_name, file_db_save_status="pending", order_id=1)
                    db.session.add(upload_items)
                    db.session.commit()
                    return 'uploading...'
                except Exception as e:
                    return(str(e))
                
            else:
                return 'file key error'
    return render_template('place_order.html', order_form=order_form, error=error, target=target)


@users_blueprint.route("/remove_file", methods=['GET', 'POST'])
def remove_file():
    
    try:
        target = os.path.join(APP_ROOT, '../static/file_uploads')
        file_id = request.args.get('file_id')
        selected_file = OrderAttachments.query.filter_by(id=file_id).first()
        attached_file_path = os.path.join(target, selected_file.file_name)

        if attached_file_path is not None:
            os.remove(attached_file_path)
            print('file removed from directory')
            db.session.delete(selected_file)
            db.session.commit()
            print('file deleted')
            if "update_orders_url" in session:
                return redirect(session['update_orders_url'])
        return request.url

    except Exception as e:
        return (str(e))


def get_current_user_id():
    return current_user.id


def get_client_order(id):

    posts = ClientPosts.query.filter_by(author_id=id).order_by(ClientPosts.id.desc()).all()
    return posts


def get_user_by_username(user_name):
    try:
        user = User.query.filter_by(username=user_name).first()
        return user
    except Exception as e:
        return (str(e))















