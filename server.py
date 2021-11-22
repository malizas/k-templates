"""Server for Photocard Template Creator"""

from flask import (Flask, render_template, request, flash, session,
                redirect, Markup)
from model import connect_to_db
import crud
# import cloudinary.uploader
import os

app = Flask(__name__)
app.secret_key = "dev"

# CLOUDINARY_KEY = os.environ['api_key']
# CLOUDINARY_SECRET = os.environ['api_secret']

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
    """Logs the user in"""
    email = request.form.get('email')
    password = request.form.get('password')

    user = crud.find_email(email)

    if user and password==user.password:
        # this will store the user's information
        session['user_id'] = user.user_id
        session["user_email"] = user.email
        flash('Log in sucessful!')
    else:
        flash('Login failed, please double check email or password')
        return redirect('/login')

    return redirect('/template_files')

@app.route('/logout', methods=["POST"])
def user_logout():
    """Logs the user out"""

    if session["user_email"]:
        session.pop("user_id", None)
        session.pop("user_email", None)
        return redirect("/")
    else:
        return redirect("/")


@app.route('/template_files')
def files():
    user_temps = crud.temp_by_user(session["user_id"])
    return render_template('files.html', user_temps=user_temps)

@app.route('/create_template', methods=["POST"])
def create_template():
    crud.create_template("arial", "black", "white", crud.find_user(session["user_id"]))

    return redirect('/template_creator')

@app.route('/template_creator')
def template_creator():
    photocards = crud.all_photocards()
    return render_template('template-creator.html', photocards=photocards)

@app.route('/template_creator/<template_id>')
def user_template(template_id):
    pc_temps = crud.template_by_pc_pick(template_id)
    photocards = crud.all_photocards()

    flash(f'user id is #{session["user_id"]}')
    flash(f' this is template #{template_id}')
    for pc in pc_temps:
        session["photocard_id"]=pc.photocard_id
        
        flash(f'this template is using photocard id {session["photocard_id"]}')
    return render_template('template-creator.html', photocards=photocards, pc_temps=pc_temps)

@app.route('/save_template', methods=["POST"])
def save_template(template_id):
    pc_temps = crud.template_by_pc_pick(template_id)
    for pc in pc_temps:
        session["photocard_id"]=pc.photocard_id

    return redirect('/template-creator')

if __name__ == '__main__':
    connect_to_db(app)
    app.run(debug=True, host='0.0.0.0')