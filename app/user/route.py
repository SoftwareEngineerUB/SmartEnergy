from app.user.user import UserObject
from flask import Blueprint, jsonify, request, Response

app_user = Blueprint('user', __name__)


@app_user.route("/user/statistics", methods=['GET'])
def getStatistics():
    month = int(request.args.get("month", '-1'))
    year = int(request.args.get("year", "-1"))
    if month == -1 or year == -1:
        return Response("Invalid request", status=400)

    userObj = UserObject(UserObject.getMockUser())
    statistics = userObj.getMonthlyStatistics(2016, 3)

    return jsonify(statistics)


@app_user.route("/user/unoptimized_devices")
def getUnoptimizedDevices():
    month = int(request.args.get("month", '-1'))
    year = int(request.args.get("year", "-1"))
    if month == -1 or year == -1:
        return Response("Invalid request", status=400)

    userObj = UserObject(UserObject.getMockUser())

    return jsonify(userObj.getUnoptimizedDevices(2015, 3))
