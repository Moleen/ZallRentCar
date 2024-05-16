from flask import Blueprint, render_template, request,redirect, url_for, jsonify
import jwt
import hashlib
from datetime import datetime,timedelta
from dbconnection import db
import os

SECRET_KEY_DASHBOARD = os.environ.get("SECRET_KEY_DASHBOARD")

dashboard = Blueprint('dashboard', __name__)

# GET METHODS
@dashboard.route('/dashboard')
def dashboard_page():
    token_receive = request.cookies.get("token")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
        user_info = db.users_admin.find_one({"username": payload["user"]})
        return render_template('dashboard/dashboard.html',user_info=user_info)
    except jwt.ExpiredSignatureError:
         return redirect(url_for("dashboard.dashboard_login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("dashboard.dashboard_login"))

@dashboard.route('/dashboard/product')
def product():
    token_receive = request.cookies.get("token")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
        user_info = db.users_admin.find_one({"username": payload["user"]})
        data = db.dataMobil.find({})
        return render_template('dashboard/product.html',user_info=user_info, data=data)
    except jwt.ExpiredSignatureError:
         return redirect(url_for("dashboard.dashboard_login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("dashboard.dashboard_login"))
    
@dashboard.route('/dashboard/product/add-data')
def addData():
    token_receive = request.cookies.get("token")
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
    
@dashboard.route('/dashboard/product/add-data', methods = ['POST'])
def addData_post():
    payload = jwt.decode(request.cookies.get("token"), SECRET_KEY_DASHBOARD, algorithms=['HS256'])
    user_info = db.users_admin.find_one({"username": payload["user"]})
    merek = request.form.get('merek')
    model = request.form.get('model')
    tahun = request.form.get('tahun')
    warna = request.form.get('warna')
    harga = request.form.get('harga')

    db.dataMobil.insert_one({
        'user' : user_info['username'],
        'merek' : merek.capitalize(),
        'model' : model.capitalize(),
        'tahun' : tahun.capitalize(),
        'warna' : warna.capitalize(),
        'harga' : harga.capitalize(),
        'status' : 'tersedia'.capitalize()
    })

    return jsonify({'result':'success'})