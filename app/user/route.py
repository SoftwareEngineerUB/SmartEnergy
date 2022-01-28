from flask import Blueprint, jsonify
from app.user.user import UserObject

app_user = Blueprint('user', __name__)


@app_user.route("/user/statistics", methods=['GET'])
def getStatistics():
    userObj = UserObject(UserObject.getMockUser())
    statistics = userObj.getMonthlyStatistics(2016, 3)

    return jsonify(statistics)


@app_user.route("/user/unoptimized_devices")
def getUnoptimizedDevices():
    userObj = UserObject(UserObject.getMockUser())

    return jsonify(userObj.getUnoptimizedDevices(2015, 3))
