
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
        email = request.form.get('email')
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


# Profile 
@app.route('/profile', methods=['GET'])
def get_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'result': 'unsuccess', 'msg': 'Token is missing'}), 401

    try:

        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = data['user_id']
        user = db.users.find_one({'user_id': user_id}, {'_id': 0, 'password': 0})
        if user:
            return jsonify({'result': 'success', 'profile': user})
        else:
            return jsonify({'result': 'unsuccess', 'msg': 'User not found'}), 404

    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'unsuccess', 'msg': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'result': 'unsuccess', 'msg': 'Invalid token'}), 401

# Edit Profil
@app.route('/profile', methods=['POST'])
def update_profile():
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({'result': 'unsuccess', 'msg': 'Token is missing'}), 401

    try:
        data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        user_id = data['user_id']
        user = db.users.find_one({'user_id': user_id})
        if user:
            updates = {
                'full_name': request.form.get('full_name', user['full_name']),
                'address': request.form.get('address', user['address']),
                'phone': request.form.get('phone', user['phone']),
                'email': request.form.get('email', user['email'])
            }
            if 'ktp_image' in request.files:
                ktp_image = request.files.get('ktp_image')
                ktp_image_path = f'ktp_images/{user_id}.jpg'
                ktp_image.save(ktp_image_path)
                updates['ktp_image_path'] = ktp_image_path

            db.users.update_one({'user_id': user_id}, {'$set': updates})
            return jsonify({'result': 'success', 'msg': 'Profile updated successfully'})
        else:
            return jsonify({'result': 'unsuccess', 'msg': 'User not found'}), 404
    except jwt.ExpiredSignatureError:
        return jsonify({'result': 'unsuccess', 'msg': 'Token has expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'result': 'unsuccess', 'msg': 'Invalid token'}), 401


app.register_blueprint(dashboard.dashboard)
app.register_blueprint(api.api)

 
if __name__ == '__main__':
    app.run(debug=True)
    # tessss