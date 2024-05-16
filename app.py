from flask import Flask,render_template,request,jsonify
import dashboard
import api
from dbconnection import db
from bson import ObjectId
import midtransclient
import random
import datetime

app = Flask(__name__)

@app.route('/')
def home():
    data = db.dataMobil.find({'status':'Tersedia'})
    return render_template('main/main.html', data = data)

@app.route('/beli/<id>')
def pesan(id):
    data = db.dataMobil.find_one({'_id': ObjectId(id)})
    snap = midtransclient.Snap(
        is_production=False,
        server_key='SB-Mid-server-ArjIt5WM6gvnMrxhx9Q3nufJ',
        client_key='SB-Mid-client-pYGOQrTmRDZCDTJt'
    )
    current_time = datetime.datetime.now()
    order_id = current_time.strftime("%Y%m%d%H%M%S")
# Prepare parameter
    param = {
        "transaction_details": {
            "order_id": order_id,
            "gross_amount": int(data['harga'])
        },
          "item_details":{
            "id" : id,
            "price" : int(data['harga']),
            "quantity" : 1,
            "name" : data['model'] + data['merek'] 
        },
          "credit_card":{
            "secure" : True
        }
    }
    transaction = snap.create_transaction(param)

    transaction_token = transaction['token']
    return render_template('main/pemesanan.html', data = data ,transaction_token =transaction_token)

@app.route('/updateCar', methods=['POST'])
def updateCar():
    db.dataMobil.update_one({'_id' : ObjectId(request.form.get('id'))},{'$set': {'status': request.form.get('statusMobil')}})
    return jsonify({
        'result':'success'
    })

app.register_blueprint(dashboard.dashboard)
app.register_blueprint(api.api)


if __name__ == '__main__':
    app.run(debug=True)