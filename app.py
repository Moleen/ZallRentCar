
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
from datetime import datetime, timedelta
from flask_mail import Mail, Message
from func import canceltransaction

SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)

app.config.from_pyfile('config.py')

mail = Mail(app)

@app.route('/')
def home():
    token_receive = request.cookies.get("tokenMain")
    data = db.dataMobil.find({'status' : 'Tersedia'})
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
        email = request.form.get('email')
        password = request.form.get('password')

        pw = hashlib.sha256(password.encode("utf-8")).hexdigest()
        user = db.users.find_one({"email": email, "password": pw})

        if user:
            payload = {
                "user_id": user['user_id'],
                "exp": datetime.now() + timedelta(hours=1)
            }
            
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')

            return jsonify({
                'result' : 'success',
                'token' : token,
            })
        
        else:
            return jsonify({

                'msg' : 'Invalid email or password'

            })
    else:

        try:
            token_receive = request.cookies.get("tokenMain")
            jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
            return redirect(url_for('home'))
        except:
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
        data = db.transaction.find({"user_id": payload["user_id"]})
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
            return render_template('main/payment.html', data = data,user_info=user_info)
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
    data_mobil = db.dataMobil.find({"id_mobil": {"$ne": id} , 'status' : 'Tersedia'})

    if data:
        data['harga'] = int(data.get('harga', 0))

    token_receive = request.cookies.get("tokenMain")

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["user_id"]})
        if user_info['verif'] != 'verifed':
            return redirect(url_for('verify_email'))
        return render_template('main/car-details.html', data=data, user_info=user_info,data_mobil =data_mobil)
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
    
@app.route('/forgot_pass')
def forgot_pass():
    return render_template('main/form_forgot_pass.html')

@app.route('/forgot_pass', methods =['POST'])
def forgot_pass_send():

    payload = {
        'exp' : datetime.now() + timedelta(minutes=30)
    }

    if request.form.get('from') == 'users':
        email = request.form.get('email')
        cek_email = db.users.find_one({'email' : email})
        if not cek_email:
            print('tesssss')
            return jsonify({
                'result':'failed',
                'message' : 'email tidak terdaftar'
            })
        
        payload['email'] = email
        payload['who'] = 'users'
        token = jwt.encode(payload, 'change_pass', algorithm='HS256')

    elif request.form.get('from') == 'admin':
        data = db.users_admin.find_one({})
        print(data)
        if data['verif'] == 'unverif':
            return jsonify({
                'message' : 'anda belum verifikasi',
            })
        payload['who'] = 'admin'
        email = data['email']
        payload['email'] = email
        token = jwt.encode(payload, 'change_pass', algorithm='HS256')

    link = f'https://good-polite-ton.glitch.me/change-password/{token}'
    html_content = f"""
                <!DOCTYPE html>
                <html>
                <head>
                    <style>
                        .container {{
                            width: 100%;
                            max-width: 600px;
                            margin: 0 auto;
                            background-color: #ffffff;
                            padding: 20px;
                            border: 1px solid #dddddd;
                            font-family: "League Spartan", sans-serif;
                        }}
                        .header {{
                            text-align: center;
                            padding: 10px 0;
                            background-color: #007bff;
                            color: white;
                        }}
                        .content {{
                            padding: 20px;
                            text-align: center;
                        }}
                        .footer {{
                            text-align: center;
                            padding: 10px 0;
                            background-color: #f6f6f6;
                            color: #999999;
                        }}
                        .button {{
                            display: inline-block;
                            padding: 10px 20px;
                            margin: 20px 0;
                            background-color: #007bff;
                            color: white;
                            text-decoration: none;
                            border-radius: 5px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>Lupa Password</h1>
                        </div>
                        <div class="content">
                            <p>Halo,</p>
                            <p>Berikut adalah link untuk mengganti password akun mu:</p>
                            <a class="button" href="{link}" style="color: white;">Reset Password</a>
                            <p>Silakan akses link berikut untuk mengubah password, link ini berlaku 30 menit</p>
                        </div>
                        <div class="footer">
                            <p>&copy; 2024 ZallRentCar. Semua hak dilindungi.</p>
                        </div>
                    </div>
                </body>
                </html>
                """

    msg = Message('Lupa Password ZallRentCar', recipients=[email], html=html_content, sender=app.config['MAIL_USERNAME'])
    mail.send(msg)
    return jsonify({
        'result' : 'success',
        'message' : 'Email berhasil dikirim'
    })

@app.route('/change-password/<token>',methods=['GET','POST'])
def method_name(token):

    cek_token = db.blacklist_token.find_one({'token' : token})
    if cek_token:
        msg = createSecreteMassage('link ganti password kadaluarsa')
        return redirect(url_for('login', msg = msg))

    if request.method == 'GET':
        try:
            jwt.decode(token, 'change_pass', algorithms=['HS256'])
            return render_template('main/from_change_password.html')
        except jwt.ExpiredSignatureError:
            msg = createSecreteMassage('link ganti password kadaluarsa')
            return redirect(url_for('login', msg = msg))
        except jwt.exceptions.DecodeError:
            msg = createSecreteMassage('link ganti password kadaluarsa')
            return redirect(url_for('login', msg = msg))
        
    elif request.method == 'POST':
        password = request.form.get('password')
        c_password = request.form.get('c_password')

        if password != c_password:
            return jsonify({
                'result' : 'fail',
                'message' : 'Password tidak sama'
            })
        elif password == '':
            return jsonify({
                'result' : 'fail',
                'message' : 'Password tidak boleh kosong'
                })
        elif len(password) < 8:
            return jsonify({
                'result' : 'fail',
                'message' : 'Password minimal 8 karakter'
                })
        else:
            pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
            try:
                payload = jwt.decode(token, 'change_pass', algorithms=['HS256'])
                if payload['who'] == 'users':
                    db.users.update_one({'email' : payload['email']},{'$set' :{'password' : pw_hash}})
                    redirect_after = '/login'
                elif payload['who'] == 'admin':
                    db.users_admin.update_one({'email' : payload['email']},{'$set' :{'password' : pw_hash}})
                    redirect_after = '/dashboard'
                
                db.blacklist_token.insert_one({'token' : token})
                return jsonify({
                    'result' : 'success',
                    'message' : 'Password berhasil diubah',
                    'redirect' : redirect_after
                })
            
            except Exception as e:
                return jsonify({
                    'result' : 'fail',
                    'message' : str(e)
                    })

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

    kode = random.randint(10000, 99999)
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Verifikasi Email</title>
    <style>
        .container {{
            width: 100%;
            max-width: 600px;
            margin: 0 auto;
            background-color: #ffffff;
            padding: 20px;
            border: 1px solid #dddddd;
            font-family: Arial, sans-serif;
        }}
        .header {{
            text-align: center;
            padding: 10px 0;
            background-color: #007bff;
            color: white;
        }}
        .content {{
            padding: 20px;
            text-align: center;
        }}
        .footer {{
            text-align: center;
            padding: 10px 0;
            background-color: #f6f6f6;
            color: #999999;
        }}
        .button {{
            display: inline-block;
            padding: 10px 20px;
            margin: 20px 0;
            background-color: #007bff;
            color: white;
            text-decoration: none;
            border-radius: 5px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Verifikasi Email Anda</h1>
        </div>
        <div class="content">
            <p>Halo,</p>
            <p>Terima kasih telah mendaftar. Berikut adalah kode verifikasi Anda:</p>
            <h2>{kode}</h2>
            <p>Silakan masukkan kode ini di halaman verifikasi untuk mengaktifkan akun Anda.</p>
        </div>
        <div class="footer">
            <p>&copy; 2024 ZallRentCar. Semua hak dilindungi.</p>
        </div>
    </div>
</body>
</html>
"""

    msg = Message('confirm email', recipients=[user['email']], html=html_content, sender=app.config['MAIL_USERNAME'])
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

 
@app.template_filter('nl2br')
def nl2br_filter(s):
    return s.replace('\n', '<br>')

if __name__ == '__main__':
    app.run(debug=True)
    # tessss