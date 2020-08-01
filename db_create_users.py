from project import db
from project.models import User

db.create_all()

# insert data
db.session.add(User("Emmanuel Sindani", "manu", "sindani254@gmail.com", "+254774631521", "Soen@30010010"))

# commit the changes
db.session.commit()
