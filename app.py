
from flask import Flask,render_template,request,jsonify, redirect,url_for
import dashboard
import api
from dbconnection import db
from bson import ObjectId
import jwt
import os
import hashlib
import midtransclient
import random
import datetime
from flask_mail import Mail, Message
from func import canceltransaction

SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    token_receive = request.cookies.get("tokenMain")
    data = db.dataMobil.find({})
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["user_id"]})
        if user_info['verif'] != 'verifed':
            return redirect(url_for('verify_email'))
        return render_template('main/home_page.html', data = data,user_info=user_info)
    except jwt.ExpiredSignatureError:
        return render_template('main/home_page.html', data = data)
    except jwt.exceptions.DecodeError:
        return render_template('main/home_page.html', data = data)


# Login tes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        pw = hashlib.sha256(password.encode("utf-8")).hexdigest()
        user = db.users.find_one({"username": username, "password": pw})

        if user:
            payload = {
                "user_id": user['user_id'],
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return jsonify({
                'result' : 'success',
                'token' : token,
            })
        
        else:
            return jsonify({

                'msg' : 'Invalid username or password'

            })
    else:

        msg = request.args.get('msg')

        try:
            payload = jwt.decode(msg, SECRET_KEY, algorithms=['HS256'])
            msg=payload['message']
            return render_template('main/login.html', msg=msg)
        except:
            return render_template('main/login.html')

@app.route('/transaksi')
def transaksiUser():
    token_receive = request.cookies.get("tokenMain")
    
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["user_id"]})
        if user_info['verif'] != 'verifed':
            return redirect(url_for('verify_email'))
        data = db.transaction.find({})
        return render_template('main/transaction.html', data = data,user_info=user_info)
    except jwt.ExpiredSignatureError:
        msg = createSecreteMassage('Akses transaksi login terlebih dahulu')
        return redirect(url_for('login', msg = msg))
    except jwt.exceptions.DecodeError:
        msg = createSecreteMassage('Akses transaksi login terlebih dahulu')
        return redirect(url_for('login', msg = msg))

@app.route('/transaksi/<id>')
def payment(id):
    token_receive = request.cookies.get("tokenMain")
    try:
        data = db.transaction.find_one({'order_id' : id})

        # CEK MOBIL SUDAH DISEWA ATAU BELUM
        data_mobil = db.dataMobil.find_one({'id_mobil' : data['id_mobil']})
        if data_mobil['status'] == 'Diproses' and data_mobil['status'] == 'Digunakan':
            canceltransaction(order_id=data['order_id'], msg='Sudah ada transaksi lain')
            return render_template('main/transactionDetail.html', data = data)
        
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["user_id"]})
        if user_info['verif'] != 'verifed':
            return redirect(url_for('verify_email'))
        token = data['transaction_token']
        if data :
            return render_template('main/payment.html', data = data, token = token,user_info=user_info)
        else:
            return redirect(url_for('transaksiUser'))
    except jwt.ExpiredSignatureError:
        msg = createSecreteMassage('Akses transaksi login terlebih dahulu')
        return redirect(url_for('login', msg = msg))
    except jwt.exceptions.DecodeError:
        msg = createSecreteMassage('Akses transaksi login terlebih dahulu')
        return redirect(url_for('login', msg = msg))
    


@app.route('/detail-mobil')
def detail():
    id = request.args.get('id')

    data = db.dataMobil.find_one({'id_mobil': id})
    if data:
        data['harga'] = int(data.get('harga', 0))

    token_receive = request.cookies.get("tokenMain")

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["user_id"]})
        if user_info['verif'] != 'verifed':
            return redirect(url_for('verify_email'))
        return render_template('main/car-details.html', data=data, user_info=user_info)
    except jwt.ExpiredSignatureError:
        return render_template('main/car-details.html', data=data)
    except jwt.exceptions.DecodeError:
        return render_template('main/car-details.html', data=data)

@app.route('/profile', methods=['GET'])
def get_profile():
    token_receive = request.cookies.get("tokenMain")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["user_id"]})
        if user_info['verif'] != 'verifed':
            return redirect(url_for('verify_email'))
        
        return render_template('main/profil.html',user_info=user_info)
    except jwt.ExpiredSignatureError:
        msg = createSecreteMassage('login terlebih dahulu')
        return redirect(url_for('login', msg = msg))
    except jwt.exceptions.DecodeError:
        msg = createSecreteMassage('login terlebih dahulu')
        return redirect(url_for('login', msg = msg))

# Edit Profil
@app.route('/profile', methods=['POST'])
def update_profile():
    token_receive = request.cookies.get("tokenMain")
    if not token_receive:
        return jsonify({'result': 'unsuccess', 'msg': 'Token is missing'}), 401

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        user = db.users.find_one({'user_id': user_id})
        if user:
            updates = {
                'username': request.form.get('username', user['username']),
                'phone': request.form.get('phone', user['phone']),
                'email': request.form.get('email', user['email'])
            }
            # Handle address separately
            address = request.form.get('address')
            if address:
                updates['address'] = address
            elif 'address' in user:
                updates['address'] = user['address']
            else:
                updates['address'] = ''

            if 'profile_image' in request.files:
                profile_image = request.files.get('profile_image')
                profile_image_path = f'static/profile_images/{user_id}.jpg'
                profile_image.save(profile_image_path)
                updates['profile_image_path'] = profile_image_path

            db.users.update_one({'user_id': user_id}, {'$set': updates})
            print(f"Profile updated for user_id: {user_id}")  # Log for debugging
            return jsonify({'result': 'success', 'msg': 'Profile updated successfully'})
        else:
            return jsonify({'result': 'unsuccess', 'msg': 'User not found'}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'unsuccess', 'msg': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'result': 'unsuccess', 'msg': 'Invalid token'}), 401


@app.route('/verify_email')
def verify_email():
    token_receive = request.cookies.get("tokenMain")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["user_id"]})
        mesagge = ''
        if user_info['verif'] == 'sending_email':
            mesagge = 'Email Sudah Terkirim, masukkan kode yang diberikan ke bawah ini'
        else:
            mesagge = 'Zallrentcar perlu tahu kalau emailmu aktif, jadi verifikasi emailmu dengan klik tombol dibawah'

        return render_template('main/verify_email.html', mesagge =mesagge, user_info = user_info)
    except jwt.ExpiredSignatureError:
        msg = createSecreteMassage('login terlebih dahulu')
        return redirect(url_for('login', msg = msg))
    except jwt.exceptions.DecodeError:
        msg = createSecreteMassage('login terlebih dahulu')
        return redirect(url_for('login', msg = msg))

@app.route('/api/verify', methods=['POST'])
def verify():
    user = db.users.find_one({'user_id' : request.form.get('user_id')})
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = 'maulana.syakhiya@gmail.com'
    app.config['MAIL_PASSWORD'] = 'dfck slpj sdww jwhx'

    mail = Mail(app)

    kode = random.randint(10000, 99999)

    msg = Message('confirm email', recipients=[user['email']], html=f'{kode}', sender=app.config['MAIL_USERNAME'])
    mail.send(msg)

    kode_hash = hashlib.sha256(str(kode).encode("utf-8")).hexdigest()
    
    db.users.update_one({'user_id' : user['user_id']},{'$set' : {'verif' : 'sending_email', 'kode' : kode_hash}})
    return jsonify({
        'msg': 'succeess'
    })

@app.route('/api/verify_kode', methods=['POST'])
def verify_kode():
    user = request.form.get('user_id')
    kode = request.form.get('kode')
    kode_hash = hashlib.sha256(kode.encode("utf-8")).hexdigest()
    result = db.users.find_one({'user_id' : user , 'kode' : kode_hash})

    print(kode_hash)
    if result:
        db.users.update_one({'user_id' : user},{'$set' : {'verif' : 'verifed'}})
        return jsonify({
            'result' : 'success'
        })
    else:
        
        return jsonify({
            'result' : 'failed',
            'msg' : 'kode verifikasi salah'
        })

def createSecreteMassage(msg):
    payload = {
            "message": msg,
        }
    msg = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return msg

app.register_blueprint(dashboard.dashboard)
app.register_blueprint(api.api)

 
if __name__ == '__main__':
    app.run(debug=True)
    # tessss