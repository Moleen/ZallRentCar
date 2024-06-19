from flask import Blueprint, render_template, request,redirect, url_for, jsonify
import jwt
import hashlib
from datetime import datetime,timedelta
from dbconnection import db
import os
import uuid
from dateutil.relativedelta import relativedelta

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
        return jsonify({
            'result' : 'failed',
            'msg' : 'username telah diubah coba lagi nanti'
        })
    else:
        exp = datetime.now() + relativedelta(month=1)
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
    

@dashboard.route('/settings/ganti_email', methods=['GET', 'POST'])
def ganti_email():

    if request.method == 'POST':
        pass

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
    file = request.files['gambar']
    merek = request.form.get('merek')
    seat = request.form.get('seat')
    transmisi = request.form.get('transmisi')
    harga = request.form.get('harga')

    if file:
        extension = file.filename.split('.')[-1]
        upload_date = datetime.now().strftime('%Y-%M-%d-%H-%m-%S')
        gambar_name = f'mobil-{upload_date}.{extension}'
        file.save(f'static/gambar/{gambar_name}')
    else:
        return jsonify({
            'result' : 'unsucces',
            'msg' : 'Masukkan gambar'
        }) 

    db.dataMobil.insert_one({
        'id_mobil' : str(id_mobil),
        'user' : user_info['username'],
        'merek' : merek.capitalize(),
        'gambar' : gambar_name,
        'seat' : seat.capitalize(),
        'transmisi' : transmisi.capitalize(),
        'harga' : harga.capitalize(),
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

    data = db.dataMobil.find_one({"id_mobil": id_mobil})

    try:
        file = request.files['gambar']
        os.remove(f'static/gambar/{data['gambar']}')
        extension = file.filename.split('.')[-1]
        upload_date = datetime.now().strftime('%Y-%M-%d-%H-%m-%S')
        gambar_name = f'mobil-{upload_date}.{extension}'
        file.save(f'static/gambar/{gambar_name}')
    except:
        gambar_name = data['gambar']

    db.dataMobil.update_one({'id_mobil' : id_mobil},
    {'$set':{
        'user' : user_info['username'],
        'merek' : merek.capitalize(),
        'gambar' : gambar_name,
        'seat' : seat.capitalize(),
        'transmisi' : transmisi.capitalize(),
        'harga' : harga.capitalize(),
        'status' : 'tersedia'.capitalize(),
    }})

    return jsonify({'result':'success'})


# list mobil
@dashboard.route('/api/daftar_mobil')
def api_daftar_mobil():
    data_mobil = list(db.dataMobil.find({}))
    for mobil in data_mobil:
        mobil['_id'] = str(mobil['_id'])  # Convert ObjectId to string
    return jsonify({'data_mobil': data_mobil})