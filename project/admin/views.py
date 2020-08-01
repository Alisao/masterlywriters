from flask import redirect, session, render_template, request, url_for, Blueprint, flash, jsonify, make_response
from flask_login import login_user, login_required, logout_user, current_user
from project.models import Admin, User, ClientPosts, IPN, OrderAttachments, bcrypt, ClientMessages, WriterFiles
from .forms import OrderForm, AdminLoginForm, AdminRegForm
from project import app, db
from werkzeug.utils import secure_filename
from flask_uploads import UploadSet, configure_uploads, ALL, DATA, DEFAULTS, patch_request_class
from flask_dropzone import Dropzone
from werkzeug.datastructures import ImmutableOrderedMultiDict
from datetime import datetime
import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
FILE_DIR = '../static/file_uploads/writer_files'
ERR_NO_FILE_SPECIFIED = 'error: no file specified'

admin_blueprint = Blueprint(
	'admin',
	__name__,
	template_folder='templates'
)

media = UploadSet('media', default_dest=lambda app: app.instance_path)
configure_uploads(app, media)
patch_request_class(app)  # set maximum file size, default is 16MB


@admin_blueprint.route("/admin/auth/session_new", methods=["GET", "POST"])
def session_new():
	error = None
	loginform = AdminLoginForm(request.form)
	regform = AdminRegForm()
	return render_template('admin_auth.html', loginform=loginform, regform=regform)



@admin_blueprint.route("/admin/auth/admin_login", methods=['GET', 'POST'])
def admin_login():
    regform = AdminRegForm()
    error = None
    loginerror = None
    loginform = AdminLoginForm(request.form)
    if request.method == 'POST':
        if loginform.validate_on_submit():
        	admin_username = loginform.username.data
        	admin_user = Admin.query.filter_by(username=admin_username).first()

        	if admin_user is not None and bcrypt.check_password_hash(admin_user.password, loginform.password.data):
        		session["admin_session_active"] = True
        		return redirect(url_for('admin.dashboard'))
        	else:
        		admin_email = Admin.query.filter_by(email=admin_username).first()

        		if admin_email is not None and bcrypt.check_password_hash(admin_email.password, loginform.password.data):
        			session["admin_session_active"] = True
        			return redirect(url_for('admin.dashboard'))
        		else:
        			loginerror = 'invalid credentials! please try again.'
        else:
            return "not validated"
    return render_template('admin_auth.html', regform=regform, loginform=loginform, error=error, loginerror=loginerror)


@admin_blueprint.route("/admin/auth/admin_logout")
def admin_logout():
	session.pop("admin_session_active", None)
	return redirect(url_for('admin.dashboard'))


@admin_blueprint.route("/admin/dashboard", methods=['GET', 'POST'])
def dashboard():
	if not 'admin_session_active' in session:
		return redirect(url_for('admin.session_new'))

	order_form = OrderForm(request.form)
	order_info = None
	orders = ClientPosts.query.order_by(ClientPosts.due_date.desc()).all()
	orders_count = len(orders)

	client_msgs = ClientMessages.query.order_by(ClientMessages.id.desc()).all()
	msg_count = len(client_msgs)

	users = db.session.query(User).all()
	users_count = len(users)

	order_files = []
	writer_files = []

	if 'show_modal' in session:

		if 'order_ID' in session:
			order_info = ClientPosts.query.filter_by(id=session['order_ID']).first()

			order_form.d_date.data = order_info.due_date.strftime("%b %d %Y" + " at " + "%H:%M" + "hrs")
			
			order_files = OrderAttachments.query.filter_by(order_id=session['order_ID']).all()
			writer_files = WriterFiles.query.filter_by(order_id=session['order_ID']).all()

	return render_template('dashboard.html', 
		client_msgs=client_msgs, msg_count=msg_count, 
		orders=orders, orders_count=orders_count,
		order_form=order_form,
		order_info=order_info,
		order_files=order_files,
		writer_files=writer_files,
		users=users,
		users_count=users_count
	)


@admin_blueprint.route("/admin/dashboard/view_order", methods=['GET', 'POST'])
def get_order():
	order_id = request.args.get('orderID')
	session['order_ID'] = order_id
	session['show_modal'] = True
	return redirect(url_for('admin.dashboard'))


@admin_blueprint.route("/admin/dashboard/take_order", methods=['GET', 'POST'])
def take_order():
	order_id = request.args.get('orderID')

	order_details = ClientPosts.query.filter_by(id=order_id).first()

	order_details.order_status = "In Progress"
	db.session.commit()
	
	session['order_taken'] = True
	flash("The order #" + str(order_id) + " on " + str(order_details.topic) + " has been assigned to you. Please start working on the assignment and make sure that the paper is finished within the given time and according to the customers instructions. The deadline is " + str(order_details.due_date))

	return redirect(url_for('admin.dashboard'))


@admin_blueprint.route("/admin/dashboard/writer_optout", methods=['GET', 'POST'])
def writer_optout():
	sku = request.args.get('opt_out_id')
	this_order = ClientPosts.query.filter_by(id=sku).first()
	this_order.order_status = "Writer pending"
	db.session.commit()

	return redirect(url_for('admin.dashboard'))


@admin_blueprint.route('/admin/dashboard/upload_files', methods=['GET', 'POST'])        
def upload_files():
    target = os.path.join(APP_ROOT, '../static/file_uploads/writer_files')    
    error = None

    if "file_urls" not in session:
    	session['file_urls'] = []

    # list to hold our uploaded file urls
    file_urls = session['file_urls']

    if request.method == 'POST':
    	if not os.path.isdir(target):
    		os.mkdir(target)
    	for key, f in request.files.items():
    		if key.startswith('file'):
    			file_name = secure_filename(f.filename)
    			f.save(os.path.join(target, file_name))
    			session['file_urls'] = file_urls

    			# append file urls
    			file_urls.append(file_name)
    return file_name


@admin_blueprint.route('/admin/dashboard/complete_order', methods=['GET', 'POST'])
def complete_order():
	order_sku = request.args.get('order_sku')
	now = datetime.now()
	last_modified = now.strftime("%b %d %Y %H:%M:%S")

	if "file_urls" in session:
		print('writer files ziko')

		for file in session['file_urls']:

			try:
				writer_files = WriterFiles(
					file_name=file,
					order_id=order_sku,
					last_modified=last_modified
				)

				db.session.add(writer_files)
				db.session.commit()

				# update order status
				this_order = ClientPosts.query.filter_by(id=order_sku).first()
				this_order.order_status = "Client Approval"
				db.session.commit()
				print("order status updated")

				session.pop('file_urls', None)
				print ("files successfully uploaded")
				return redirect(url_for('admin.dashboard'))
			except Exception as e:
				return str(e)
			
	return redirect(url_for('admin.dashboard'))
