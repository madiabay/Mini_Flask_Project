from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import yaml

app = Flask(__name__)

# DB configuration
db = yaml.safe_load(open('db.yaml'))
app.config['MYSQL_HOST'] = db['mysql_host']
app.config['MYSQL_USER'] = db['mysql_user']
app.config['MYSQL_PASSWORD'] = db['mysql_password']
app.config['MYSQL_DB'] = db['mysql_db']
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        form = request.form
        name = form['name']
        age = form['age']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO employee(name, age) VALUES(%s, %s);", (name, age))
        cursor.connection.commit()
        return 'SUCCESS!', 201
    return render_template('index.html')

@app.route('/employees/')
def employees():
    cursor = mysql.connection.cursor()
    result_value = cursor.execute("SELECT * FROM employee;")
    if result_value > 0:
        employees = cursor.fetchall()
        return render_template('employee.html', employees_html=employees)
    return 'EMPTY'

if __name__ == '__main__':
    app.run(debug=True, port=8000)