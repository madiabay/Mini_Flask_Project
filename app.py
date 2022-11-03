from flask import Flask, render_template, request, session, flash
from flask_mysqldb import MySQL
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap
import yaml, secrets

app = Flask(__name__)
Bootstrap(app)

secret = secrets.token_urlsafe(32)

# DB configuration
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

app.secret_key = secret

mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            form = request.form
            name = form['name']
            age = form['age']
            cursor = mysql.connection.cursor()
            # name = generate_password_hash(name)
            cursor.execute("INSERT INTO employee(name, age) VALUES(%s, %s);", (name, age))
            cursor.connection.commit()
            flash('Your data is successfully inserted', 'success')
        except:
            flash('The inserting is failed', 'danger')
    return render_template('index.html')

@app.route('/employees/')
def employees():
    cursor = mysql.connection.cursor()
    result_value = cursor.execute("SELECT * FROM employee;")
    if result_value > 0:
        employees = cursor.fetchall()
        session['username'] = employees[0]['name']
        # return str(check_password_hash(employees[7]['name'], '.amelebalgamspor124:D'))
        return render_template('employee.html', employees_html=employees)
    return 'EMPTY'

if __name__ == '__main__':
    app.run(debug=True, port=8000)