from flask import Blueprint, render_template, request,redirect, url_for, jsonify,json
from dbconnection import db
import jwt
import hashlib
from datetime import datetime,timedelta
from bson import ObjectId
import midtransclient
import requests
import uuid
import os
from validate_email import validate_email_or_fail

SECRET_KEY = os.environ.get("SECRET_KEY")


api = Blueprint('api', __name__)

@api.route('/api/search-dashboard')
def searchDahboard():
    search = request.args.get('search')
    data = db.dataMobil.find({'merek' : {'$regex': search, '$options': 'i'}} , {'_id': 0})
    return list(data)

@api.route('/api/create_transaction', methods = ['POST'])
def create_transaction():
    id_mobil = request.form.get('id_mobil')
    hari = request.form.get('hari')
    user = request.form.get('user')
    order_id = str(uuid.uuid1())
    dateRent = datetime.now().strftime("%d-%B-%Y")
    endRent = datetime.now() + timedelta(days=int(hari))
    endRent = endRent.strftime("%d-%B-%Y")
    data_mobil = db.dataMobil.find_one({'id_mobil': id_mobil})
    item_name = f"{data_mobil['merek']} {data_mobil['model']}"

    snap = midtransclient.Snap(
    is_production=False,
    server_key='SB-Mid-server-ArjIt5WM6gvnMrxhx9Q3nufJ',
    client_key='SB-Mid-client-pYGOQrTmRDZCDTJt'
    )
    param = {
            "transaction_details": {
                "order_id": order_id,
                "gross_amount": int(data_mobil['harga']) * int(hari)
            },
            "item_details": [{
                "id": id_mobil,
                "price": data_mobil['harga'],
                "quantity": int(hari),
                "name": item_name
            }],
            "customer_details": {
                "first_name": user,
                "email": "taytai4869@gmail.com",
            }
        }



    transaction = snap.create_transaction(param)
    transaction_token = transaction['token']

    transakasi = {
        'user' : user,
        'user_id' : '123123123123',
        'order_id' : order_id,
        'id_mobil' : id_mobil,
        'transaction_token' : transaction_token,
        'item' : item_name,
        'total' : int(data_mobil['harga']) * int(hari),
        'lama_rental' : f'{hari} hari',
        'date_rent' : dateRent,
        'end_rent' : endRent,
        'status' : 'unpaid',
    }
    db.transaction.insert_one(transakasi)

    
    return jsonify({
        'id' : order_id
    })

@api.route('/api/transaction-success', methods=['POST'])
def transactionSuccess():
    idcar = request.form.get('idcar')
    orderid = request.form.get('orderid')
    
    if request.form.get('from') == 'user':
        dataUpdate = {
            'status': 'Diproses',
            'order_id' : orderid
            }
    else:
        dataUpdate = {
            'status': 'Digunakan',
            'order_id' : orderid
            }
        
    db.dataMobil.update_one({'id_mobil' : idcar},{'$set': dataUpdate })
    db.transaction.update_one({'order_id' : orderid},{'$set': {'status' : 'sudah bayar'} })
    
    return jsonify({
        'result':'success'
    })

@api.route('/api/cancelPayment', methods=['POST'])
def cancelPayment():
    order_id = request.form.get('order_id')
    url = f"https://api.sandbox.midtrans.com/v2/{order_id}/cancel"

    headers = {
        "accept": "application/json",
        "Authorization" : "Basic U0ItTWlkLXNlcnZlci1BcmpJdDVXTTZndm5NcnhoeDlRM251Zko6"}

    requests.post(url, headers=headers)
    
    db.transaction.delete_one({'order_id' : order_id})
    return jsonify({
        'result' :'success'
    })

@api.route('/register', methods=['POST'])
def reg():
    username = request.form.get('username')
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    user_id = str(uuid.uuid1())

    pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()

    if db.users.find_one({'username': username}):
        return jsonify({
            'result' : 'unsucces',
            'msg' : 'username sudah ada'
        })
    elif db.users.find_one({'email': email}):
        return jsonify({
            'result' : 'unsucces',
            'msg' : 'email sudah ada'
        })
    else:
        try:
            validate_email_or_fail(check_format=True, email_address=email, smtp_timeout=10, dns_timeout=10,)
        except:
            return jsonify({
                'result' : 'unsucces',
                'msg' : 'email tidak valid'
            })
        db.users.insert_one({
            'user_id' : user_id,
            'username' : username,
            'email' : email,
            'phone' : phone,
            'password' : pw_hash,
        })
        payload = {
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(seconds=60 * 60 * 24),
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({
            "result": "success",
            "token": token
        })

# @api.route('/api/change-status', methods=['POST'])
# def changeStatus():
#     orderid=request.form.get('orderid')
#     status=request.form.get('status')
    
#     if checkStatusTrans(orderid):
#         db.dataMobil.update_one({'order_id' : orderid})
#     return




# def checkStatusTrans(orderid):
#     data = db.transaction.find_one({'order_id':orderid})
#     if data.status == 'sudah bayar':
#         return True
