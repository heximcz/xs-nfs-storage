from flask import (
    Blueprint,
    request,
    render_template,
    redirect,
    g,
    session,
    url_for
)
from flask_bcrypt import Bcrypt
from src.Config import LoadConfig

auth = Blueprint('auth', __name__)
bcrypt = Bcrypt()

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def get_id(self):
        return f'{self.id}'

    def get_username(self):
        return f'{self.username}'

    def get_password(self):
        return f'{self.password}'

# new password generate via /doc/BCrypt.py and save it to the config.yml
config = LoadConfig()
user = User(id=1, username='admin', password=config.env("web_password"))

@auth.before_request
def before_request():
    g.user = None

    if 'user_id' in session:
        username = user.get_username()
        g.user = username

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        session.pop('user_id', None)

        username = request.form['username']
        password = request.form['password']
        
        if username == user.get_username() and bcrypt.check_password_hash(user.get_password(), password):
            session.permanent = True
            session['user_id'] = user.get_id()
            return redirect(url_for('views.home'))

        return redirect(url_for('auth.login'))

    return render_template('login.html')

@auth.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('views.home'))