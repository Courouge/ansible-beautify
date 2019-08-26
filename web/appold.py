from flask import Flask, render_template, flash
from flask_bootstrap import Bootstrap
from flask_appconfig import AppConfig
from flask_wtf import Form, RecaptchaField
from flask_wtf.file import FileField
from wtforms import TextField, HiddenField, ValidationError, RadioField,\
    BooleanField, SubmitField, IntegerField, FormField, validators
from wtforms.validators import Required

def create_app(configfile=None):

    app = Flask(__name__)
    Bootstrap(app)

    @app.route('/')
    def hello_world():
       return render_template('main.html')
    return app

if __name__ == '__main__':
    create_app().run(debug=True,host='0.0.0.0')
