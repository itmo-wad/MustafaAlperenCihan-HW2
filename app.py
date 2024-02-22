from flask import Flask, render_template, request, redirect, session, url_for
from pymongo import MongoClient
import hashlib
from werkzeug.utils import secure_filename
import os

# Flask app initialization
app = Flask(__name__)
app.secret_key = 'my_super_secret_key'

# MongoDB setup
client = MongoClient('mongodb://localhost:27017/')
db = client.user_auth_db
users_collection = db.users

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route for login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        user = users_collection.find_one({"username": username, "password": hashed_password})

        if user:
            session['username'] = user['username']
            return redirect(url_for('profile'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Check if username already exists
        existing_user = users_collection.find_one({"username": username})
        if existing_user is None:
            users_collection.insert_one({
                "username": username,
                "password": hashed_password,
                "name": "",
                "email": "",
                "profile_pic_url": "images/default.jpg"
            })
            return redirect('/')
        else:
            return "Username already exists"

    return render_template('register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/profile')
def profile():
    if 'username' in session:
        user = users_collection.find_one({"username": session['username']})
        return render_template('profile.html', user=user)
    else:
        return redirect('/')

@app.route('/change_password', methods=['POST'])
def change_password():
    if 'username' not in session:
        return redirect('/')

    user = users_collection.find_one({"username": session['username']})
    current_password = request.form['current_password']
    new_password = request.form['new_password']
    confirm_password = request.form['confirm_password']
    hashed_current_password = hashlib.sha256(current_password.encode()).hexdigest()

    if user['password'] != hashed_current_password:
        return "Current password is incorrect.", 401
    if new_password != confirm_password:
        return "New passwords do not match.", 400

    hashed_new_password = hashlib.sha256(new_password.encode()).hexdigest()
    users_collection.update_one({"username": session['username']}, {"$set": {"password": hashed_new_password}})

    return redirect('/profile')


@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'username' not in session:
        return redirect('/')

    if request.method == 'POST':
        # Process the profile update form submission
        username = session['username']
        name = request.form.get('name', '')
        email = request.form.get('email', '')
        file = request.files.get('profile_picture')

        update_data = {"name": name, "email": email}

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            update_data['profile_pic_url'] = url_for('static', filename=os.path.join('uploads', filename))

        users_collection.update_one({"username": username}, {"$set": update_data})
        return redirect('/profile')
    else:
        if 'username' in session:
            user = users_collection.find_one({"username": session['username']})
            return render_template('update_profile.html', user=user)
        else:
            return redirect('/')

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
