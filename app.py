from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from os.path import join, dirname
from dotenv import load_dotenv
import jwt
import hashlib
from datetime import datetime,timedelta
from pymongo import MongoClient
import midtransclient
import dashboard

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


SECRET_KEY = os.environ.get("SECRET_KEY")
MONGODB_URI = os.environ.get("MONGODB_URI")
DB =  os.environ.get("DB")

client = MongoClient(MONGODB_URI)
db = client[DB]


app = Flask(__name__)
app.register_blueprint(dashboard.dashboard)

@app.route("/")
def home():
    token_receive = request.cookies.get("token")

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["user"]})
        return render_template('main/index.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
         return redirect(url_for("login", msg="Your token has expired"))
    except jwt.exceptions.DecodeError:
        return redirect(url_for("login"))
    
# GET METHODS

@app.route("/login",  methods = ["GET"])
def login():
    msg = request.args.get("msg")
    return render_template('main/login.html', msg = msg)

@app.route("/daftar" , methods = ["GET"])
def signup():
    return render_template('main/signup.html')


#POST METHOD

@app.route("/daftar" ,methods = ['POST'])
def daftar_post():
    email = request.form.get("email")
    user = request.form.get("username")
    password = request.form.get("password")

    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    result = db.users.find_one({'username': user})
    if result:
        return jsonify({
            "result": "fail",
            "msg": "user telah ada"
        })
    else:
        db.users.insert_one({'email' : email, 'username': user, 'password' :pw_hash})
        payload = {
            "user": user,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({
            "result": "success",
            "token": token,
        })
    
@app.route("/login" ,methods = ['POST'])
def login_post():
    user = request.form.get("username")
    password = request.form.get("password")

    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
    result = db.users.find_one({'username': user, 'password': pw_hash})
    if result:
        payload = {
            "user": user,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({
            "result": "success",
            "token": token
        })
    else:
        return jsonify({
            'result' : 'unsucces',
            'msg' : 'password atau username salah'
        })

if __name__ == '__main__':
    app.run(debug=True)