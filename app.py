from flask import Flask, render_template, session, request
import pymysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Leyno'

conn = pymysql.connect(host='tsuts.tskoli.is', port=3306, user='1410022280',                               password='Shar1110', database='1410022280_verk7')
# https://pythonspot.com/login-authentication-with-flask/

@app.route('/')
def index():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    p = cur.fetchall()
    
    for i in p:
        print(i[2])
    return render_template("index.html")

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        n = request.form['notandanafn']
        p = request.form['password']
    
    cur = conn.cursor()
    cur.execute("SELECT count(user) FROM users where user = %s and pass=%s",(n,p))
    p = cur.fetchone()
    if p[0] == 1:
        session['logged_in'] = n

        return render_template("rett.html")
    else:
        return render_template("rangt.html")

@app.route('/nyskra')
def nyskra():
    return render_template("nyskra.html")

@app.route('/add', methods=['GET','POST'])
def add():
    if request.method == 'POST':
        n = request.form['notandanafn']
        pw = request.form['password']
        nafn = request.form['nafn']

        cur = conn.cursor()
        cur.execute("SELECT count(*) FROM users where user = %s",(n))
        p = cur.fetchone()
        if p[0] != 1:
            cur.execute("INSERT INTO users(user,pass,nafn) VALUES(%s,%s,%s)",(n,pw,nafn))
            conn.commit()
            cur.close()
            return render_template("nyr.html")

        else:
            return render_template("tekid.html")

@app.route('/utskra')
def utskra():
    listi = []
    session['logged_in'] = listi

    return render_template("utskra.html")

@app.route('/vefur')
def vefur():
    cur = conn.cursor()
    cur.execute("SELECT * FROM users")
    p = cur.fetchall()
    for i in p:
        if i[0] in session['logged_in']:
            nafn = i[2]
        
    return render_template("vefur.html", p=p, n=nafn)


if __name__ == '__main__':
    app.run(debug=True)