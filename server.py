"""Server for Photocard Template Creator"""

from flask import (Flask, render_template, request, flash, session,
                redirect, Markup)
from model import connect_to_db
import crud

app = Flask(__name__)
app.secret_key = "dev"

@app.route('/')
def homepage():
    return render_template('homepage.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/user', methods=['POST'])
def user_registration():
    email = request.form.get('email')
    password = request.form.get('password')

    if crud.find_email(email):
        flash('Use already exist, please try again or login')
        return redirect('/login')
    else:
        crud.create_user(email, password)
        flash('Registration complete, please login')
        return redirect('/login')

@app.route('/login', methods=['POST'])
def user_login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.find_email(email)

    if user and password==user.password:
        session['user_id'] = user.user_id
        flash('Log in sucessful!')
    else:
        flash('Login failed, please double check email or password')
        return redirect('/login')

    return redirect('/template')


@app.route('/template')
def template_creator():
    return render_template('template.html')


if __name__ == '__main__':
    connect_to_db(app, "photocards")
    app.run(debug=True, host='0.0.0.0')