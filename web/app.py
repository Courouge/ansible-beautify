from flask import Flask, render_template, request
from wtforms import Form, StringField, TextField, TextAreaField, validators, StringField, SubmitField
from wtforms.validators import DataRequired

# App config.
DEBUG = True
app = Flask(__name__)

class ProcessForm(Form):
    submit_button = SubmitField('Do Something')

@app.route('/')
def test():
    form = ProcessForm()
    if form['submit_button'] == 'Do Something':
         if 'download' in request.form:
            print("go")

    else:
        return render_template('main.html')

if __name__ == '__main__':
   app.run(debug = True)