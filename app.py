from flask import Flask,render_template,request,jsonify, redirect,url_for
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
    data = db.dataMobil.find({})
    return render_template('main/main.html', data = data)

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


app.register_blueprint(dashboard.dashboard)
app.register_blueprint(api.api)

 
if __name__ == '__main__':
    app.run(debug=True)