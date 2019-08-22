from flask import Flask, render_template, request
from wtforms import Form, StringField, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired

from flask_bootstrap import Bootstrap

app = Flask(__name__)

Bootstrap(app)

@app.route('/')
def hello_world():
    return render_template('main.html')

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0')