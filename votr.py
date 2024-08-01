from flask import (
    Flask, render_template, request, flash, redirect, url_for, session, jsonify
)
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, Users, Topics, Polls, Options, UserPolls
from flask_migrate import Migrate
from flask_admin import Admin
from admin import AdminView, TopicView
from api.api import api
import config
from celery import Celery

def make_celery(app):
    celery = Celery(app.import_name, broker=config.CELERY_BROKER)
    celery.conf.update(votr.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
        
    celery.Task = ContextTask

    return celery

votr = Flask(__name__)
votr.register_blueprint(api)
votr.config.from_object('config')

db.init_app(votr)
#db.create_all(app=votr)

migrate = Migrate(votr, db, render_as_batch=True)

celery = make_celery(votr)

admin = Admin(votr, name='Dashboard', index_view=TopicView(Topics, db.session, url='/admin', endpoint='admin'))
admin.add_view(AdminView(Users, db.session))
admin.add_view(AdminView(Polls, db.session))
admin.add_view(AdminView(Options, db.session))

@votr.route('/')
def home():
    return render_template('index.html')
@votr.route('/signup', methods = ['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']

        password = generate_password_hash(password, method="pbkdf2")
        try : 
            user = Users(email=email,username=username,password=password)

            db.session.add(user)
            db.session.commit()

            flash('Thanks for joining, please signin now')
            return redirect(url_for('home'))
        except Exception as e:
            flash('User already exists')
            return redirect(url_for('home'))
    return render_template('signup.html')

@votr.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    user = Users.query.filter_by(username=username).first()

    if user :
        password_hash = user.password
        if check_password_hash(password_hash, password):
            session['user'] = username
            flash('Login Successful')
        else:
            flash('Password incorrect')
    else:
        flash('Username not found','error')

    return redirect(request.args.get('next') or url_for('home'))

@votr.route('/logout')
def logout():
    if 'user' in session:
        session.pop('user')

        flash('We hope to see you again!')

    return redirect(url_for('home'))

@votr.route('/polls', methods=['GET'])
def polls():
    return render_template('polls.html')

@votr.route('/polls/<poll_name>')
def poll(poll_name):

    return render_template('index.html')

