from . import db
import re
from datetime import datetime
from . import config
from vars import old_file


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    browser_pushid = db.Column(db.Text)
    push_email = db.Column(db.Integer, default='1')
    push_web = db.Column(db.Integer, default='1')
    alert_deadline = db.Column(db.Integer, default='1')


def deadlines(username):
    try:
        read_file = open(old_file, 'r', encoding='utf-8').read()
        dates = re.findall('.*(20[0-9]{2}-\d{2}-\d{2}).*\.\s.*#%s' % username, read_file)
        dates = [datetime.strptime(date, '%Y-%m-%d') for date in dates]
        now = datetime.now()

        past_dates = [date for date in dates if date < now]
        last_deadline = max(date for date in dates if date < now) if past_dates else 'None'

        future_dates = [date for date in dates if date > now]
        next_deadline = min(date for date in dates if date > now) if future_dates else 'None'

        return {'last': str(last_deadline)[:10], 'next': str(next_deadline)[:10]}

    except FileNotFoundError:

        return {'last': 'None', 'next': 'None'}
