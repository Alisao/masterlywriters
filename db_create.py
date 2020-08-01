from project import db
from project.models import ClientPosts, User, Admin, OrderAttachments, WriterFiles, ClientMessages, IPN
from datetime import datetime, timedelta

d_date = datetime.now() + timedelta(hours=int(6))

# create the database and the bd tables
db.create_all()

# add user
db.session.add(User("Emmanuel Sindani", "manu", "sindani254@gmail.com", "+254774631521", "Soen@30010010"))

# add order
db.session.add(
	ClientPosts(
		'data structures',
		'computer science',
		'article',
		'Undergraduate',
		datetime.now() + timedelta(hours=6),
		2,
		'(2500 words)',
		'double',
		"APA6",
		5,
		'Create an argumentative essay outline (not the essay, just the outline)',
		'pending_payment',
		'pending_payment',
		34.50,
		1
	)
)

# commit the changes
db.session.commit()
