import jwt
import requests
from dbconnection import db
from dateutil.relativedelta import relativedelta
from datetime import datetime

def createSecretMessage(msg, SECRET_KEY, redirect='/'):
    payload = {
            "message": msg,
            "redirect" : redirect
        }
    msg = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return msg

def canceltransaction(order_id,msg):
    url = f"https://api.sandbox.midtrans.com/v2/{order_id}/cancel"

    headers = {
        "accept": "application/json",
        "Authorization" : "Basic U0ItTWlkLXNlcnZlci1BcmpJdDVXTTZndm5NcnhoeDlRM251Zko6"}

    requests.post(url, headers=headers)
    
    expire_at = datetime.utcnow()
    db.transaction.update_one({'order_id' : order_id},{'$set' : {'expired' : expire_at, 'status' : 'Dibatalkan','pesan': msg}})
