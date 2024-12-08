from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# تكوين الاتصال بقاعدة البيانات
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'  # استبدلها باسم المستخدم في قاعدة بياناتك
app.config['MYSQL_PASSWORD'] = 'salma'  # استبدلها بكلمة المرور إذا كانت موجودة
app.config['MYSQL_DB'] = 'votingsystem'

mysql = MySQL(app)

@app.route('/')
def index():
    # جلب البيانات من قاعدة البيانات
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM votes')
    projects = cur.fetchall()
    cur.close()
    return render_template('index.html', projects=projects)

@app.route('/vote', methods=['POST'])
def vote():
    project_id = request.form['project_id']
    cur = mysql.connection.cursor()

    # زيادة التصويت للمشروع بناءً على project_id
    cur.execute('UPDATE votes SET votecount = votecount + 1 WHERE id = %s', (project_id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)
