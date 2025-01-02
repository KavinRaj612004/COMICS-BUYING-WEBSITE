from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
  
app = Flask(__name__)
app.secret_key = 'xyzsdfg'
  
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'hari'
app.config['MYSQL_PORT'] = 3307  
  
mysql = MySQL(app)
  
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/action')
def action():
    return render_template('action.html')

@app.route('/romance')
def romance():
    return render_template('romance.html')

@app.route('/fantasy')
def fantasy():
    return render_template('fantasy.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/ordering', methods=['GET', 'POST'])
def ordering():
    message = ''  # Corrected variable name
    if request.method == 'POST' and all(key in request.form for key in ['username', 'email', 'phno', 'address', 'pincode', 'volumes', 'card']):
        Username = request.form['username']
        Email = request.form['email']
        Phno = request.form['phno']
        Address = request.form['address']
        Pincode = request.form['pincode']
        Volumes = request.form['volumes']
        Card = request.form['card']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM ordering WHERE Username = %s', (Username,))
        order = cursor.fetchone()
        if not re.match(r'[^@]+@[^@]+\.[^@]+', Email):
            message = 'Invalid email address !'
        elif not all([Username, Email, Phno, Address, Pincode, Volumes, Card]):  # Using all() for readability
            message = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO ordering VALUES (%s, %s, %s, %s, %s, %s, %s)',
                           (Username, Email, Phno, Address, Pincode, Volumes, Card))
            mysql.connection.commit()
            message = 'You have successfully placed the order !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('ordering.html', message=message)  # Pass message to template

@app.route('/success')
def success():
    return render_template('success.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE email = %s AND password = %s', (email, password,))
        user = cursor.fetchone()
        if user:
            session['loggedin'] = True
            session['userid'] = user['userid']
            session['username'] = user['username']
            session['email'] = user['email']
            message = 'Logged in successfully !'
            return render_template('user.html', message=message)  # Pass message to template
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message=message)  # Pass message to template

@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and all(key in request.form for key in ['username', 'password', 'email']):
        userName = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM login WHERE email = %s', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address !'
        elif not all([userName, password, email]):  # Using all() for readability
            message = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO login VALUES (NULL, %s, %s, %s)', (userName, email, password,))
            mysql.connection.commit()
            message = 'You have successfully registered !'
    elif request.method == 'POST':
        message = 'Please fill out the form !'
    return render_template('register.html', message=message)  # Pass message to template

if __name__ == "__main__":
    app.run(port=3307)  # Change the port number to 3307
