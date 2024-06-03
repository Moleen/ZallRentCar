from flask import Flask,render_template,request,jsonify, redirect,url_for
import dashboard
import api
from dbconnection import db
from bson import ObjectId
import jwt
import os
import midtransclient
import random
import datetime

SECRET_KEY = os.environ.get("SECRET_KEY")

app = Flask(__name__)

@app.route('/')
def home():
    token_receive = request.cookies.get("token")
    data = db.dataMobil.find({})
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"user_id": payload["user_id"]})
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
        user = db.users_admin.find_one({"username": username, "password": password})
        if user:
            payload = {
                "user": username,
                "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
            return jsonify({
                'token' : token
            })
        
        else:
            return jsonify({
                'result' : 'username ga ada'
            })
        
    return render_template('main/login.html')

@app.route('/transaksi')
def transaksiUser():
    data = db.transaction.find({})
    return render_template('main/transaction.html', data = data)

@app.route('/transaksi/<id>')
def payment(id):
    data = db.transaction.find_one({'order_id' : id})
    token = data['transaction_token']
    if data :
        return render_template('main/payment.html', data = data, token = token)
    else:
        return redirect(url_for('transaksiUser'))

@app.route('/detail-mobil')
def detail():
    id = request.args.get('id')
    data = db.dataMobil.find_one({'_id' : ObjectId(id)})
    print(id)
    return render_template('main/car-details.html', data = data)

@app.route('/setting')
def setting():
    return render_template('main/profil.html')

app.register_blueprint(dashboard.dashboard)
app.register_blueprint(api.api)

 
if __name__ == '__main__':
    app.run(debug=True)