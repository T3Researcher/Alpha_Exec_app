from flask import Flask, render_template, redirect, url_for, flash, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from university_canvas_api import get_canvas_courses, get_canvas_assignments, get_canvas_modules, get_account_calendars


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'


@app.route('/')
def home():
    return 'Hello, World!'


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if user:
            flash('Username already exists. Please choose a different one.')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password, method='sha256')
        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. You can now log in.')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(username=username).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid username or password. Please try again.')
            return redirect(url_for('login'))

        flash(f'Welcome, {username}!')
        return redirect(url_for('home'))

    return render_template('login.html')


@app.route('/canvas_courses')
def canvas_courses():
    courses = get_canvas_courses()
    return render_template('canvas_courses.html', courses=courses)


@app.route('/canvas_assignments/<int:course_id>')
def canvas_assignments(course_id):
    assignments = get_canvas_assignments(course_id)
    if assignments:
        return render_template('canvas_assignments.html', assignments=assignments)
    else:
        return "Error: Unable to fetch assignments.", 500


@app.route('/canvas_modules/<int:course_id>')
def canvas_modules(course_id):
    modules = get_canvas_modules(course_id)
    if modules:
        return render_template('canvas_modules.html', modules=modules)
    else:
        return "Error: Unable to fetch modules.", 500


@app.route('/account_calendars')
def account_calendars():
    account_calendars = get_account_calendars()
    return render_template('account_calendars.html', account_calendars=account_calendars)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
