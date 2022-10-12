from flask import Flask, redirect, flash, url_for
from datetime import timedelta
from flask_wtf.csrf import CSRFProtect, CSRFError

app = Flask(__name__)
app.config['SECRET_KEY'] = '6h1o9Q59#eOT&ne$#%T*9mAej1&Nlns5'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)

csrf = CSRFProtect(app)

@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    flash('Platnost formuláře vypršela. Zkuste to znovu.', category='error')
    return redirect(url_for('views.home'))

def vdi_app():

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    return app