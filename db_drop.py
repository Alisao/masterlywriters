from project import db
from project.models import *


# create the database and the bd tables
db.drop_all()


# commit the changes
db.session.commit()
