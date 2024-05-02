"""
This file defines the database models
"""

import datetime
from .common import db, Field, auth
from pydal.validators import *


def get_user_email():
    return auth.current_user.get('email') if auth.current_user else None

def get_time():
    return datetime.datetime.utcnow()

db.define_table('keow',
                Field('keow_content', 'text'),
                Field('user_email', default=get_user_email),
                Field('created_on', 'datetime', default=get_time),
)

db.define_table('thumb',
                Field('keow_id', 'reference keow'),
                Field('rater', default=get_user_email),
                Field('thumb', 'integer', default=0),
)

db.commit()
