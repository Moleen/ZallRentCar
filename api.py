from flask import Blueprint, render_template, request,redirect, url_for, jsonify,json
from dbconnection import db
import jwt
import hashlib
from datetime import datetime,timedelta




api = Blueprint('api', __name__)

@api.route('/api/search-dashboard')
def searchDahboard():
    search = request.args.get('search')
    data = db.dataMobil.find({'merek' : {'$regex': search, '$options': 'i'}} , {'_id': 0})
    return list(data)