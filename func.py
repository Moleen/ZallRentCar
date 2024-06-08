import jwt

def createSecretMessage(msg, SECRET_KEY, redirect='/'):
    payload = {
            "message": msg,
            "redirect" : redirect
        }
    msg = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return msg
