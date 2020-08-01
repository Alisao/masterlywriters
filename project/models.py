from project import app, db
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from project import bcrypt
from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import relationship


class Admin(db.Model):

    __tablename__ = "admin"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, name, username, email, phone_number, password):
        self.name = name
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')


class User(db.Model):

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    posts = relationship("ClientPosts", backref="author")
    messages = relationship("ClientMessages", backref="author")

    def __init__(self, name, username, email, phone_number, password):
        self.name = name
        self.username = username
        self.email = email
        self.phone_number = phone_number
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def get_reset_token(self, expires_sec=3600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception as e:
            return (str(e))
        return User.query.get(user_id)


class ClientPosts(db.Model):

    __tablename__ = "client_posts"

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String, nullable=False)
    discipline = db.Column(db.String, nullable=False)
    paper_type = db.Column(db.String, nullable=False)
    ac_level = db.Column(db.String, nullable=False)
    due_date = db.Column(db.TIMESTAMP, nullable=False)
    total_pages = db.Column(db.Integer, nullable=False)
    word_count = db.Column(db.String, nullable=False)
    spacing = db.Column(db.String, nullable=False)
    paper_format = db.Column(db.String, nullable=False)
    sources = db.Column(db.Integer, nullable=False)   
    instructions = db.Column(db.String, nullable=False)
    rev_instructions = db.Column(db.String, nullable=True)
    order_status = db.Column(db.String, nullable=False)
    payment_status = db.Column(db.String, nullable=False)
    grand_total = db.Column(db.Float(precision=2), nullable=False)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    files = relationship("OrderAttachments", backref="client_posts", uselist=False)

    def __init__(self, \
            topic, \
            discipline, \
            paper_type, \
            ac_level, due_date, total_pages, word_count, spacing, paper_format, sources, \
            instructions, \
            order_status, \
            payment_status, grand_total, author_id):
        self.topic = topic
        self.discipline = discipline
        self.paper_type = paper_type
        self.due_date = due_date
        self.ac_level = ac_level
        self.total_pages = total_pages
        self.word_count = word_count
        self.spacing = spacing
        self.paper_format = paper_format
        self.sources = sources
        self.instructions = instructions
        self.order_status = order_status
        self.payment_status = payment_status
        self.grand_total = grand_total
        self.author_id = author_id

    def __repr__(self):
        return '<id - {}>'.format(self.id)       


class OrderAttachments(db.Model):

    __tablename__ = "attachments"

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    file_db_save_status = db.Column(db.String, nullable=False)
    last_modified = db.Column(db.TIMESTAMP, nullable=False)
    order_id = db.Column(db.Integer, ForeignKey('client_posts.id'), nullable=False)

    def __init__(self, file_name, file_db_save_status, last_modified, order_id):
        self.file_name = file_name
        self.file_db_save_status = file_db_save_status
        self.last_modified = last_modified
        self.order_id = order_id

    def __repr__(self):
        '<id - {}>'.format(self.id)


class WriterFiles(db.Model):

    __tablename__ = "writer_files"

    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    last_modified = db.Column(db.TIMESTAMP, nullable=False)
    order_id = db.Column(db.Integer, ForeignKey('client_posts.id'), nullable=False)

    def __init__(self, file_name, last_modified, order_id):
        self.file_name = file_name
        self.last_modified = last_modified
        self.order_id = order_id

    def __repr__(self):
        '<id - {}>'.format(self.id)


class ClientMessages(db.Model):
    
    __tablename__ = "client_messages"

    id = db.Column(db.Integer, primary_key=True)
    message_details = db.Column(db.String, nullable=False)
    date_sent = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    order_id = db.Column(db.Integer, nullable=True)
    author_id = db.Column(db.Integer, ForeignKey('users.id'))
    msg_read = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, message_details, date_sent, order_id, author_id, msg_read):
        self.message_details = message_details
        self.date_sent = date_sent
        self.order_id = order_id
        self.author_id = author_id
        self.msg_read = msg_read

    def __repr__(self):
        '<id - {}>'.format(self.id)


class UserMessages(db.Model):
    
    __tablename__ = "user_messages"

    id = db.Column(db.Integer, primary_key=True)
    sender_name = db.Column(db.String, nullable=False)
    sender_email = db.Column(db.String, nullable=False)
    sender_phone = db.Column(db.String, nullable=True)
    message_details = db.Column(db.String, nullable=False)
    date_sent = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    msg_read = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, sender_name, sender_email, sender_phone, message_details, date_sent, msg_read):
        self.sender_name = sender_name
        self.sender_email = sender_email
        self.sender_phone = sender_phone
        self.message_details = message_details
        self.date_sent = date_sent
        self.msg_read = msg_read

    def __repr__(self):
        '<id - {}>'.format(self.id)


class IPN(db.Model):

    __tablename__ = "paypal_ipn"

    id = db.Column(db.Integer, primary_key=True)
    payer_id = db.Column(db.Integer, nullable=False)
    payer_email = db.Column(db.String, nullable=False)
    payer_first_name = db.Column(db.String, nullable=False)
    payer_last_name = db.Column(db.String, nullable=False)
    payment_date = db.Column(db.TIMESTAMP(timezone=True), nullable=False)
    payment_gross = db.Column(db.NUMERIC(5,2), nullable=False)
    payment_fee = db.Column(db.NUMERIC(5,2), nullable=False)
    payment_status = db.Column(db.String, nullable=False)
    txn_id = db.Column(db.String, nullable=False)

    def __init__(self,
            payer_id,
            payer_email,
            payer_first_name,
            payer_last_name,
            payment_date,
            payment_fee,
            payment_gross,
            payment_status,
            txn_id):
        self.payer_id = payer_id
        self.payer_email = payer_email
        self.payer_first_name = payer_first_name
        self.payer_last_name = payer_last_name
        self.payment_date = payment_date
        self.payment_gross = payment_gross
        self.payment_fee = payment_fee
        self.payment_status = payment_status
        self.txn_id = txn_id        
