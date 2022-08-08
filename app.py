from flask import Flask

from API import (login, register, user)

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello World"

@app.route("/registerUser", methods=["POST"])
def register_user():
    return register.register_user()

@app.route("/validateUser", methods=["POST"])
def validate_user():
    return login.validate_user()

@app.route("/getLocationNames", methods=["GET"])
def get_location_names():
    return user.get_location_names()

@app.route("/searchTicket", methods=["POST"])
def search_tickets():
    return user.search_tickets()

@app.route("/getUserInfo", methods=["POST"])
def get_user_info():
    return user.get_user_info()

@app.route('/updateUserPassword', methods=['POST'])
def update_user_password():
    return user.update_user_password()

@app.route("/updateUserInfo", methods=["POST"])
def update_user_info():
    return user.update_user_info()

@app.route("/getUserID", methods=['POST'])
def get_user_id():
    return user.get_user_id()

@app.route("/getPurchaseSummary", methods=["POST"])
def get_purchase_summary():
    return user.get_purchase_summary()

@app.route("/getTripSummary", methods=["POST"])
def get_trip_summary():
    return user.set_trip_summary()

@app.route("/getSeatLayout", methods=["POST"])
def get_seat_layout():
    return user.set_seat_layout()

@app.route("/getPurchaseTicket", methods=["POST"])
def get_purchase_ticket():
    return user.set_purchased_ticket()

@app.route('/checkOut', methods=['POST'])
def check_out():
    return user.check_out()

if __name__ == '__main__':
    app.run(debug=True)
