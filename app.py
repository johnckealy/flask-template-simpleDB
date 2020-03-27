from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
import os
import random



app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
if 'FLASK_ENV' in os.environ and os.environ['FLASK_ENV'] == 'development':
    from dotenv import load_dotenv
    POSTGRES = {
        'user': os.environ['PG_USER'],
        'pw': os.environ['PG_PWD'],
        'db': os.environ['PG_DATABASE'],
        'host': 'localhost',
        'port': '5432',
    }
    load_dotenv()
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES

heroku = Heroku(app)
db = SQLAlchemy(app)


# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)

    def __init__(self, email):
        self.email = email



@app.route('/')
def index():
    data = db.session.query(User)
    return render_template('index.html', data=data)

@app.route('/populate')
def prereg():
    emails = ['johnny@email.com', 'jack@email.com', 'billy@email.com', 'jim@email.com']
    email = random.sample(emails, 1)[0]
    reg = User(email)
    db.session.add(reg)
    db.session.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    #app.debug = True
    app.run()
