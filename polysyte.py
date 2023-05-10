from flask import Flask, render_template, request, url_for, redirect
import pyqrcodeng as qr
import io, sys
from os import urandom
from time import time
from data import db_session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from data.users import User
import hashlib
import barcode
import time

db_session.global_init("bases/pass.db")

def get_svg(data):
    url = qr.create(data)
    buffer = io.BytesIO()
    url.svg(buffer, xmldecl=False, scale=8)
    return buffer.getvalue().decode()

class Passer:
    def __init__(self):
        # [userid, id]
        self.__pass = []
        self.counter = 0

    def add(self, userid):
        id = int.from_bytes(urandom(16), sys.byteorder)
        self.__pass.append((userid, id))
        self.counter += 1
        if self.counter >= 100:
            self.__pass = self.__pass[-50:]
            self.counter = len(self.__pass)
        return id

    def pop(self, id):
        flag = 0
        for i in range(len(self.__pass)):
            if self.__pass[i][1] == id:
                flag = 1
                del self.__pass[i]
                break
        self.counter -= 1
        return '{"should_open": ' + str(flag) + '}'

    # debug
    @property
    def codes(self):
        return self.__pass

app = Flask(__name__)
app.config['SECRET_KEY'] = 'AWs@@nWH$XT^3c#%328Z-u3HyHBZ!%J?'
login_manager = LoginManager()
login_manager.init_app(app)
passer = Passer()

@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)

@app.route('/')
def mainpage():
    return render_template('main.html', data='')

@app.route('/profile')
def profile():
    return render_template('profile.html', data='', barcode=barcode.Code128(str(current_user.barcode)).render(writer_options={'module_width':1, 'compress': True}).decode())

@app.route('/qr')
@login_required
def getqr():
    if (not current_user.rights is None) and 'q' in current_user.rights:
        return render_template('main.html', data='<div style="text-align: center">' + get_svg(passer.add(current_user.id)) + '</div>')
    else:
        return render_template('main.html', data='<div style="text-align: center"><h1 style="color:#ff0000">Аккаунт не подтвержден</h1></div>')

# degug
@app.route('/codes')
def getcodes():
    return render_template('main.html', data='<br>'.join(map(lambda x: str(x[0]) + ': ' + str(x[1]), passer.codes)))

@app.route('/open/<data>')
def popqr(data):
    return passer.pop(int(data))

@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == 'GET':
        return render_template('login.html', data='')
    if request.method == 'POST':
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.login == request.form['login']).first()
        if user and user.passwordhash == hashlib.sha256(request.form['password'].encode()).hexdigest():
            login_user(user)
            return redirect('/')
        else:
            return 'incorrect username or password'

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')

    if request.method == 'POST':
        db_sess = db_session.create_session()
        print(request.files, request)
        file = request.files['img']
        print(file)
        imgname = f'{str(time.time())}.jpg'
        file.save('static/images/'+imgname)
        user = User(
            name_surname=request.form['fio'].strip(),
            login=request.form['login'].strip(),
            group_facult=request.form['facul'].strip(),
            barcode=(int(request.form['barcode'].strip()) if request.form['barcode'].strip() else 0),
            blank_id=request.form['blank_id'].strip(),
            passwordhash=hashlib.sha256(request.form['password'].strip().encode()).hexdigest(),
            photoid = imgname
        )
        if not user.name_surname or not user.passwordhash or not user.login or not user.group_facult:
            return redirect('/signup')
        db_sess.add(user)
        db_sess.commit()
        login_user(user)
        return redirect('/')

@app.route('/dev/<method>')
def dev(method):
    if method == 'is_logged':
        if current_user.is_authenticated:
            return str(current_user.login)
        else:
            return 'anon - V'
    
@app.route('/logout')
def logout():
    logout_user() 
    return redirect('/')

app.run("0.0.0.0", 80)
