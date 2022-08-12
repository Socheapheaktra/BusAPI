from flask import Flask

from API import (login, register, user, admin)

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

@app.route('/getAdminInfo', methods=['POST'])
def get_admin_info():
    return admin.get_user_info()

@app.route("/updateAdminInfo", methods=["POST"])
def update_admin_info():
    return admin.update_user_info()

@app.route("/updateAdminPassword", methods=["POST"])
def update_admin_password():
    return admin.update_password()

@app.route('/showTransaction', methods=["GET"])
def show_transaction():
    return admin.show_transaction()

@app.route("/searchTransaction", methods=['POST'])
def search_transaction():
    return admin.search_transaction()

@app.route("/getDistinctUserID", methods=["GET"])
def get_unique_user_id():
    return admin.get_distinct_user_id()

@app.route('/showTransactionDetail', methods=['POST'])
def show_transaction_detail():
    return admin.show_transaction_detail()

@app.route('/updateTransaction', methods=["POST"])
def update_transaction():
    return admin.update_transaction()

@app.route('/getTripDetail', methods=["POST"])
def get_trip_detail():
    return admin.get_trip_detail()

@app.route("/showUserTable", methods=["GET"])
def show_user_table():
    return admin.show_user_table()

@app.route("/showTripTable", methods=["GET"])
def show_trip_table():
    return admin.show_trip_table()

@app.route('/showBusTable', methods=['GET'])
def show_bus_table():
    return admin.show_bus_table()

@app.route('/getActiveTrip', methods=["GET"])
def get_active_trip():
    return admin.get_active_trip()

@app.route('/getActiveBus', methods=['POST'])
def get_active_bus():
    return admin.get_active_bus()

@app.route('/addTrip', methods=['POST'])
def add_trip():
    return admin.add_trip()

@app.route('/updateTrip', methods=["POST"])
def update_trip():
    return admin.update_trip()

@app.route('/endTrip', methods=["POST"])
def end_trip():
    return admin.end_trip()

@app.route('/admin/getLocationNames', methods=['GET'])
def add_location_dropdown():
    return admin.get_location_names()

@app.route('/admin/addUser', methods=['POST'])
def add_user():
    return admin.add_user()

@app.route('/admin/updateUser', methods=["POST"])
def update_user():
    return admin.update_user()

@app.route('/admin/getUsername', methods=["GET"])
def get_username():
    return admin.get_username()

@app.route("/admin/removeUser", methods=["POST"])
def remove_user():
    return admin.remove_user()

@app.route("/admin/addBus", methods=["POST"])
def add_bus():
    return admin.add_bus()

@app.route("/admin/updateBus", methods=["POST"])
def update_bus():
    return admin.update_bus()

if __name__ == '__main__':
    app.run(debug=True)
