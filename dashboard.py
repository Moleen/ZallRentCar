from flask import Blueprint, render_template, request,redirect, url_for, jsonify,current_app
import jwt
import hashlib
from datetime import datetime,timedelta
from dbconnection import db
import os
import uuid
from dateutil.relativedelta import relativedelta
from flask_mail import Message
import random

SECRET_KEY_DASHBOARD = os.environ.get("SECRET_KEY_DASHBOARD")

dashboard = Blueprint('dashboard', __name__)

# GET METHODS
@dashboard.route('/dashboard')
def dashboard_page():
    token_receive = request.cookies.get("tokenDashboard")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
        user_info = db.users_admin.find_one({"username": payload["user"]})
        jumlah_mobil = db.dataMobil.count_documents({})
        jumlah_transaksi = db.transaction.count_documents({})
        datenow = datetime.now().strftime("%Y")
        total_transaksi = list(db.transaction.find({'status': 'sudah bayar','date_rent' : {'$regex': datenow, '$options': 'i'}},{'_id': 0, 'total': 1}))
        total_values = sum([trans['total'] for trans in total_transaksi])
        
        transaksi_pertahun = db.transaction.find({'status': 'sudah bayar'})

        tahun_transaksi = []
        for data in transaksi_pertahun:
            date = datetime.strptime(data['date_rent'], "%d-%B-%Y")
            tahun = str(date.year)

            if tahun not in tahun_transaksi:
                tahun_transaksi.append(tahun)

        tahun_transaksi.sort()       
        return render_template('dashboard/dashboard.html',
                               user_info=user_info,
                                 jumlah_mobil = jumlah_mobil,
                                 jumlah_transaksi= jumlah_transaksi,
                                 total_transaksi = total_values,
                                 tahun_transaksi = tahun_transaksi)
    except jwt.ExpiredSignatureError:
         return redirect(url_for("dashboard.dashboard_login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("dashboard.dashboard_login"))

@dashboard.route('/data_mobil')
def data_mobil():
    token_receive = request.cookies.get("tokenDashboard")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
        user_info = db.users_admin.find_one({"username": payload["user"]})
        data = db.dataMobil.find({})
        return render_template('dashboard/data_mobil.html',user_info=user_info, data=data)
    except jwt.ExpiredSignatureError:
         return redirect(url_for("dashboard.dashboard_login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("dashboard.dashboard_login"))

@dashboard.route('/data_mobil/edit')
def data_mobilDetail():
    id = request.args.get('id')
    token_receive = request.cookies.get("tokenDashboard")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
        user_info = db.users_admin.find_one({"username": payload["user"]})
        data = db.dataMobil.find_one({'id_mobil' : id})
        return render_template('dashboard/edit_mobil.html',user_info=user_info, data=data)
    except jwt.ExpiredSignatureError:
         return redirect(url_for("dashboard.dashboard_login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("dashboard.dashboard_login"))

@dashboard.route('/transaction')
def transaction():
    token_receive = request.cookies.get("tokenDashboard")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
        user_info = db.users_admin.find_one({"username": payload["user"]})
        data = db.transaction.find({})
        return render_template('dashboard/transaction.html',user_info=user_info, data=data)
    except jwt.ExpiredSignatureError:
         return redirect(url_for("dashboard.dashboard_login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("dashboard.dashboard_login"))

@dashboard.route('/settings')
def setting():
    token_receive = request.cookies.get("tokenDashboard")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
        user_info = db.users_admin.find_one({"username": payload["user"]})
        data = db.transaction.find({})
        return render_template('dashboard/setting.html',user_info=user_info, data=data)
    except jwt.ExpiredSignatureError:
         return redirect(url_for("dashboard.dashboard_login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("dashboard.dashboard_login"))
    
@dashboard.route('/settings/change_username', methods=['POST'])
def change_username():
    new_username = request.form.get('new_username')
    username = request.form.get('username')
    data = db.users_admin.find_one({'username' : username})
    if datetime.now() < data['expired_username']:
        print('tes')
        return jsonify({
            'result' : 'failed',
            'msg' : 'username telah diubah coba lagi nanti'
        })
    else:
        exp = datetime.now() + relativedelta(months=1)
        db.users_admin.update_one({'username' : username}, {'$set' : {'username' : new_username, 'expired_username' : exp}})
        payload = {
            "user": new_username,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY_DASHBOARD, algorithm="HS256")
        return jsonify({
            "result": "success",
            "token": token
        })
    

@dashboard.route('/settings/change_email', methods=['GET', 'POST'])
def ganti_email():
    email = request.form.get('new_email')

    if request.method == 'POST':

        if request.form.get('mtd') == 'add_email':
            db.users_admin.update_one({'username' : request.form.get('username')},{'$set' :{'email' : email , 'verif' : 'unverif'}})
            return({
                'result' : 'success',
            })
        
        elif request.form.get('mtd') == 'send_verif':
            user_info = db.users_admin.find_one({'username' : request.form.get('username')})
            try:
                send_verification(email=user_info['email'],username=request.form.get('username'))
                return jsonify({
                    'result' : 'success',
                    'msg' : 'kirim verif success'
                })
            
            except Exception as e:
                return jsonify({
                    'result' : 'gagal',
                    'msg' : f'gagal : {str(e)}'
                })
        elif request.form.get('mtd') == 'verif':
            try:
                verif(kode=request.form.get('kode'),user=request.form.get('username'))
                return jsonify({
                    'result' : 'success',
                    'msg' : 'verif success'
                })
            
            except Exception as e:
                return jsonify({
                    'result' : 'gagal',
                    'msg' : f'gagal : {str(e)}'
                })
    
        else:
            db.users_admin.update_one({'username' : request.form.get('username')},{'$set' :{'email' : email}})
            return({
                'result' : 'success',
            })

    else:
        token_receive = request.cookies.get("tokenDashboard")
        try:
            payload = jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
            user_info = db.users_admin.find_one({"username": payload["user"]})
            return render_template('dashboard/change_email.html',user_info=user_info)
        except jwt.ExpiredSignatureError:
            return redirect(url_for("dashboard.dashboard_login", msg="Your token has expired"))
        except jwt.exceptions.DecodeError:
            return redirect(url_for("dashboard.dashboard_login"))
        
@dashboard.route('/settings/change_password', methods=['POST'])
def change_password():
    old_pass = request.form.get('password_lama')
    new_pass = request.form.get('password_baru')
    username = request.form.get('username')

    if old_pass == '':
        return jsonify({
            'result' : 'gagal',
            'msg' : 'password lama tidak boleh kosong'
        })
    elif new_pass == '':
        return jsonify({
            'result' : 'gagal',
            'msg' : 'password baru tidak boleh kosong'
        })
    elif len(new_pass) < 6:
        return jsonify({
            'result' : 'gagal',
            'msg' : 'password baru minimal 6 karakter'
        })
    
    pw_hash = hashlib.sha256(old_pass.encode("utf-8")).hexdigest()

    data = db.users_admin.find_one({'username' : username})
    
    if data['password'] == pw_hash:

        pw_hash_new = hashlib.sha256(new_pass.encode("utf-8")).hexdigest()
        db.users_admin.update_one({'username' : username},{'$set': {'password' : pw_hash_new}})
        return jsonify({
            'result' : 'success',
            'msg' : 'password berhasil di ganti'
        })
    
    else:
            
        return jsonify({
            'result' : 'gagal',
            'msg' : f'gagal : password salah'
        })
    
@dashboard.route('/data_mobil/add-data')
def addData():
    token_receive = request.cookies.get("tokenDashboard")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
        user_info = db.users_admin.find_one({"username": payload["user"]})
        return render_template('dashboard/tambahdata.html',user_info=user_info)
    except jwt.ExpiredSignatureError:
         return redirect(url_for("dashboard.dashboard_login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("dashboard.dashboard_login"))

@dashboard.route('/dashboard-login', methods = ['GET'])
def dashboard_login():
    token_receive = request.cookies.get("tokenDashboard")
    try:
        jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
        return redirect(url_for("dashboard.dashboard_page"))
    except jwt.ExpiredSignatureError:
        return render_template('dashboard/login.html')
    except jwt.exceptions.DecodeError:
        return render_template('dashboard/login.html')


# POST METHODS
@dashboard.route('/dashboard-login', methods = ['POST'])
def dashboard_login_post():
    user = request.form.get("username")
    password = request.form.get("password")
    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    result = db.users_admin.find_one({'username': user, 'password': pw_hash})
    if result:
        payload = {
            "user": user,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY_DASHBOARD, algorithm="HS256")
        return jsonify({
            "result": "success",
            "token": token
        })
    else:
        return jsonify({
            'result' : 'unsucces',
            'msg' : 'password atau username salah'
        })

@dashboard.route('/data_mobil/add-data', methods = ['POST'])
def addData_post():

    payload = jwt.decode(request.cookies.get("tokenDashboard"), SECRET_KEY_DASHBOARD, algorithms=['HS256'])
    user_info = db.users_admin.find_one({"username": payload["user"]})
    id_mobil = uuid.uuid1()
    merek = request.form.get('merek')
    seat = request.form.get('seat')
    transmisi = request.form.get('transmisi')
    harga = request.form.get('harga')
    desc = request.form.get('desc')

    if merek == '':
        return jsonify({
            'result' : 'unsucces',
            'msg' : 'merek tidak boleh kosong'
            })
    elif seat == '':
        return jsonify({
            'result' : 'unsucces',
            'msg' : 'seat tidak boleh kosong'
            })
    elif transmisi == '':
        return jsonify({
            'result' : 'unsucces',
            'msg' : 'transmisi tidak boleh kosong'
            })
    elif harga == '':
        return jsonify({
            'result' : 'unsucces',
            'msg' : 'harga tidak boleh kosong'
        })

    try:
        file = request.files['gambar']
        extension = file.filename.split('.')[-1]
        upload_date = datetime.now().strftime('%Y-%M-%d-%H-%m-%S')
        gambar_name = f'mobil-{upload_date}.{extension}'
        file.save(f'static/gambar/{gambar_name}')
    except Exception as e:
        return jsonify({
            'result' : 'unsucces',
            'msg' : f'Masukkan gambar : {e}'
        }) 

    db.dataMobil.insert_one({
        'id_mobil' : str(id_mobil),
        'user' : user_info['username'],
        'merek' : merek.capitalize(),
        'gambar' : gambar_name,
        'seat' : seat.capitalize(),
        'transmisi' : transmisi.capitalize(),
        'harga' : harga,
        'desc' : desc.capitalize(),
        'status' : 'tersedia'.capitalize(),
    })

    return jsonify({'result':'success'})

@dashboard.route('/data_mobil/update-data', methods = ['POST'])
def updateData_post():

    payload = jwt.decode(request.cookies.get("tokenDashboard"), SECRET_KEY_DASHBOARD, algorithms=['HS256'])
    user_info = db.users_admin.find_one({"username": payload["user"]})
    id_mobil = request.form.get('id_mobil')
    merek = request.form.get('merek')
    seat = request.form.get('seat')
    transmisi = request.form.get('transmisi')
    harga = request.form.get('harga')
    desc = request.form.get('desc')

    data = db.dataMobil.find_one({"id_mobil": id_mobil})

    try:
        file = request.files['gambar']
        if os.path.exists(f"static/gambar/{data['gambar']}"):
            os.remove(f"static/gambar/{data['gambar']}")
        extension = file.filename.split('.')[-1]
        upload_date = datetime.now().strftime('%Y-%M-%d-%H-%m-%S')
        gambar_name = f'mobil-{upload_date}.{extension}'
        file.save(f'static/gambar/{gambar_name}')
        print(gambar_name)
    except Exception as e:
        gambar_name = data['gambar']
        print(f'gambar lama {e}')

    db.dataMobil.update_one({'id_mobil' : id_mobil},
    {'$set':{
        'user' : user_info['username'],
        'merek' : merek.capitalize(),
        'gambar' : gambar_name,
        'seat' : seat.capitalize(),
        'transmisi' : transmisi.capitalize(),
        'harga' : harga.capitalize(),
        'desc' : desc,
        'status' : 'tersedia'.capitalize(),
    }})

    return jsonify({'result':'success'})


@dashboard.route('/transaction/add_transaction')
def add_transaction():
    token_receive = request.cookies.get("tokenDashboard")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
        user_info = db.users_admin.find_one({"username": payload["user"]})
        data = db.dataMobil.find({'status' : 'Tersedia'})
        return render_template('dashboard/add_transaction.html',user_info=user_info, data =data)
    except jwt.ExpiredSignatureError:
         return redirect(url_for("dashboard.dashboard_login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("dashboard.dashboard_login"))


# list mobil
@dashboard.route('/api/daftar_mobil')
def api_daftar_mobil():
    data_mobil = list(db.dataMobil.find({}))
    for mobil in data_mobil:
        mobil['_id'] = str(mobil['_id'])  # Convert ObjectId to string
    return jsonify({'data_mobil': data_mobil})


def send_verification(email,username):
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
            <p>&copy; 2024 Perusahaan Anda. Semua hak dilindungi.</p>
        </div>
    </div>
</body>
</html>
"""
    
    msg = Message('confirm email', recipients=[email], html=html_content, sender=current_app.config['MAIL_USERNAME'])
    mail =current_app.extensions['mail']
    mail.send(msg)
    kode_hash = hashlib.sha256(str(kode).encode("utf-8")).hexdigest()
    db.users_admin.update_one({'username' : username},{'$set' : {'verif' : 'sending_email', 'kode' : kode_hash}})
    print('mengirim kode sukses')

def verif(user,kode):
    kode_hash = hashlib.sha256(str(kode).encode("utf-8")).hexdigest()
    result = db.users_admin.find_one({'username' : user,'kode' : kode_hash})
    if result:
        db.users_admin.update_one({'username' : user},{'$set': {'verif' : 'verifed'}})


    
