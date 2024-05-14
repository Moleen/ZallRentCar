from flask import Blueprint, render_template, request,redirect, url_for, jsonify
import os
from os.path import join, dirname
from dotenv import load_dotenv
import jwt
import hashlib
from datetime import datetime,timedelta
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


SECRET_KEY_DASHBOARD = os.environ.get("SECRET_KEY_DASHBOARD")
MONGODB_URI = os.environ.get("MONGODB_URI")
DB =  os.environ.get("DB")

client = MongoClient(MONGODB_URI)
db = client[DB]

dashboard = Blueprint('dashboard', __name__)

# GET METHODS
@dashboard.route('/dashboard')
def dashboard_page():
    token_receive = request.cookies.get("token")
    try:
        payload = jwt.decode(token_receive, SECRET_KEY_DASHBOARD, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["user"]})
        return render_template('dasboard/index.html',user_info=user_info)
    except jwt.ExpiredSignatureError:
         return redirect(url_for("dashboard.dashboard_login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("dashboard.dashboard_login"))

@dashboard.route('/dashboard-login', methods = ['GET'])
def dashboard_login():
    return render_template('dasboard/login.html')


# POST METHODS
@dashboard.route('/dashboard-login', methods = ['POST'])
def dashboard_login_post():
    user = request.form.get("username")
    password = request.form.get("password")

    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    result = db.users.find_one({'username': user, 'password': pw_hash})
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