from flask import Blueprint, jsonify

from app.meter.meter import Meter
from app.models import User
from app.models.db import db

app_meter = Blueprint('app_contents', __name__)


@app_meter.route('/api/get/devices', methods=['GET'])
def getProductImage():
    username = 'mock-user'
    user = db.session.query(User).filter_by(username=username).first()
    meter = Meter(user)

    return jsonify({})

