from flask import Blueprint, render_template, request,redirect, url_for, jsonify,json
from dbconnection import db
import jwt
import hashlib
from datetime import datetime,timedelta
import midtransclient
import requests
import uuid
import os
from func import createSecretMessage, canceltransaction


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
    data_mobil = db.dataMobil.find_one({'id_mobil': id_mobil})

    user = request.form.get('user_id')
    data_user = db.users.find_one({'user_id': user})

    stat = db.transaction.find_one({'user_id': user, 'status': 'unpaid'})
    if stat:
        return jsonify({'status': 'unpaid_transaction', 'message': 'anda memiliki transaksi yang belum dibayar, batalkan transaksi sebelumnya terlebih dahulu untuk melanjutkan pemesanan'})

    elif user:
        order_id = str(uuid.uuid1())
        hari = request.form.get('hari')
        dateRent = datetime.now().strftime("%d-%B-%Y")
        endRent = datetime.now() + timedelta(days=int(hari))
        endRent = endRent.strftime("%d-%B-%Y")
        item_name = f"{data_mobil['merek']}"

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
                    "first_name": data_user['username'],
                    "email": data_user['email'],
                }
            }

        transaction = snap.create_transaction(param)
        transaction_token = transaction['token']

        transakasi = {
            'user_id' : data_user['user_id'],
            'order_id' : order_id,
            'id_mobil' : id_mobil,
            'penyewa' : data_user['username'],
            'transaction_token' : transaction_token,
            'item' : item_name,
            'total' : int(data_mobil['harga']) * int(hari),
            'lama_rental' : f'{hari} hari',
            'date_rent' : dateRent,
            'end_rent' : endRent,
            'status' : 'unpaid',
        }

        db.transaction.insert_one(transakasi)
        db.dataMobil.update_one({'id_mobil': id_mobil},{'$set':{'status_transaksi' : 'pembayaran'}})
        
        return jsonify({
            'status' : 'success',
            'id' : order_id
        })
    
    else:
        msg = createSecretMessage('Login terlebih dahulu untuk memesan', SECRET_KEY=SECRET_KEY,redirect=f'/detail-mobil?id={id_mobil}')
        return redirect(url_for('login',msg = msg))
    

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
    try:
        canceltransaction(order_id=order_id, msg='Dibatalkan sendiri')
        return jsonify({
            'result' : 'success'
        })
    except:
        return jsonify({
            'result' : 'failed'
            })
    
    

@api.route('/register', methods=['POST'])
def reg():
    username = request.form.get('username')
    email = request.form.get("email")
    password = request.form.get("password")
    phone = request.form.get("phone")
    user_id = str(uuid.uuid1())

    if len(username) < 8:
        return jsonify({
            'result' : 'ejected',
            'msg' : 'Username minimal 8 karakter'
            })
    elif not username[0].isalpha():
        return jsonify({
            'result' : 'ejected',
            'msg' : 'Username harus diawali dengan huruf'
            })
    elif not username.replace('.', '').replace('_', '').isalnum():
        return jsonify({
            'result' : 'ejected',
            'msg' : 'Username tidak valid'
            })
    elif username == '':
        return jsonify({
            'result' : 'ejected',
            'msg' : 'Username tidak boleh kosong'
            })
    elif password == '':
        return jsonify({
            'result' : 'ejectedPW',
            'msg' : 'Password tidak boleh kosong'
            })
    elif email == '':
        return jsonify({
            'result' : 'ejectedEmail',
            'msg' : 'Email tidak boleh kosong'
            })
    elif db.users.find_one({'username': username}):
        return jsonify({
            'result' : 'ejected',
            'msg' : 'username sudah ada'
        })
    elif db.users.find_one({'email': email}):
        return jsonify({
            'result' : 'ejectedEmail',
            'msg' : 'email sudah ada'
        })
    elif len(password) < 8:
        return jsonify({
            'result' : 'ejectedPW',
            'msg' : 'Password minimal 8 karakter'
            })
    elif phone == '':
        return jsonify({
            'result' : 'ejectedPhone',
            'msg' : 'Nomor telepon tidak boleh kosong'
            })
    else:
        pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        db.users.insert_one({
            'user_id' : user_id,
            'username' : username,
            'email' : email,
            'phone' : phone,
            'password' : pw_hash,
            'verif' : 'unverifed'
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
    
@api.route('/api/confirmPesanan', methods=['POST'])
def confirmPesanan():
    id_mobil = request.form.get('id_mobil')
    db.transaction.update_one({'id_mobil' : id_mobil},{'$set':{'status_mobil':'diambil'}})
    db.dataMobil.update_one({'id_mobil' : id_mobil},{'$set':{'status':'Digunakan'}})
    return jsonify({
        'result' : 'success'
    })

@api.route('/api/confirmKembali', methods=['POST'])
def confirmKembali():
    id_mobil = request.form.get('id_mobil')

    # cek akhir rental
    data_mobil =  db.dataMobil.find_one({'id_mobil' : id_mobil})
    data =  db.transaction.find_one({'order_id' : data_mobil['order_id']})
    if data['end_rent'] != datetime.now().strftime("%d-%B-%Y"):
        return jsonify({
            'result' : 'unsuccess',
            'msg' : 'tanggal pengembalian tidak sesuai'
            })
    db.transaction.update_one({'id_mobil' : id_mobil},{'$set':{'status_mobil':'selesai'}})
    db.dataMobil.update_one({'id_mobil' : id_mobil},{'$set':{'status':'Tersedia'}})
    return jsonify({
        'result' : 'success'
    })
@api.route('/api/delete_mobil', methods=['POST'])
def delete_mobil():
    id_mobil = request.form.get('id_mobil')
    data = db.dataMobil.find_one({'id_mobil' : id_mobil})
    db.dataMobil.delete_one({'id_mobil' : id_mobil})
    os.remove(f'static/gambar/{data['gambar']}')
    return jsonify({
        'result' : 'success'
    })

@api.route('/api/ambilpendapatan', methods=['POST'])
def ambilPendapatan():
    date = request.form.get('tahun')
    data = db.transaction.find({ 'status' : "sudah bayar" , 'date_rent' : {'$regex': date, '$options': 'i'}})

    total = {month: 0 for month in range(1, 13)}
    
    for dt in data:
        for month in range(1,13):
            bulan = datetime.strptime(dt['date_rent'], "%d-%B-%Y")
            if bulan.month == month:
                total[month] += int(dt['total'])
    
    return jsonify(total)

@api.route('/api/get_transaksi')
def get_transaksi():
    date = datetime.now().strftime('%Y')

    data = db.transaction.find({'status' : "sudah bayar" ,'date_rent' : {'$regex': date, '$options': 'i'}})

    total = {month: 0 for month in range(1, 13)}
    for dt in data:
        for month in range(1,13):
            bulan = datetime.strptime(dt['date_rent'], "%d-%B-%Y")
            if bulan.month == month:
                total[month] += 1
    
    print(total)
    return jsonify(total)


@api.route('/api/filter_transaksi', methods=['POST'])
def filter_transaksi():
    mtd = request.form.get('mtd')

    if mtd == 'fTanggal':
        tanggal = request.form.get('date')
        data = db.transaction.find({'date_rent' : tanggal}, {'_id': 0})
        return list(data)
    
    elif mtd == 'fPaid' :
        data = db.transaction.find({'status' : 'sudah bayar'}, {'_id': 0})
        return list(data)
    elif mtd == 'fUnpaid':
        data = db.transaction.find({'status' : 'Dibatalkan'}, {'_id':0})
        return list(data)
    



    

@api.route('/api/check_username', methods=['POST'])
def check_username():
    username = request.form.get('username')

    if len(username) < 8:
        return jsonify({
            'result' : 'ejected',
            'msg' : 'Username minimal 8 karakter'
            })
    elif db.users.find_one({'username': username}):
        return jsonify({
            'result' : 'ejected',
            'msg' : 'Username sudah ada'
        })
    elif not username[0].isalpha():
        return jsonify({
            'result' : 'ejected',
            'msg' : 'Username harus diawali dengan huruf'
            })
    elif not username.replace('.', '').replace('_', '').isalnum():
        return jsonify({
            'result' : 'ejected',
            'msg' : 'Username tidak valid'
            })
    else:
        return jsonify({
            'result' : 'available'
        })