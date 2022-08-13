from myDB import mydb, mycursor
from flask import jsonify, request
from datetime import datetime
import time

def get_username():
    try:
        sql = 'SELECT user_name FROM users'
        mycursor.execute(sql)
    except Exception as e:
        response = {
            "data": None,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        username_list = list()
        result = mycursor.fetchall()
        for username in result:
            username_list.append(username[0])

        response = {
            "data": username_list,
            "status": True,
            "message": "Call Success"
        }
        return jsonify(response)

def add_user():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "username" not in req or "password" not in req or "email" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    username_list = list()
    email_list = list()
    try:
        sql = 'SELECT user_name, email FROM users'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for data in result:
            username_list.append(data[0])
            email_list.append(data[1])
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    if req['username'] in username_list:
        response = {
            "data": req,
            "status": False,
            "message": "Username already taken!"
        }
        return jsonify(response)
    if req['password'] == "":
        response = {
            "data": req,
            "status": False,
            "message": "Password cannot be empty!"
        }
        return jsonify(response)
    if req['email'] == "":
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Email Address"
        }
        return jsonify(response)
    if req['email'] in email_list:
        response = {
            "data": req,
            "status": False,
            "message": "This Email address already been used"
        }
        return jsonify(response)
    try:
        sql = 'INSERT INTO users (user_name, user_pass, email) ' \
              'VALUES (%s, %s, %s)'
        values = [req['username'], req['password'], req['email'], ]
        mycursor.execute(sql, values)
        mydb.commit()
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        response = {
            "data": req,
            "status": True,
            "message": "Your new account has been created!"
        }
        return jsonify(response)

def update_user():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "username" not in req or "password" not in req or "email" not in req \
            or "phone" not in req or "role" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    try:
        username_list = list()
        sql = 'SELECT user_name FROM users'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for username in result:
            username_list.append(username[0])
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)

    if req['username'] not in username_list:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Username"
        }
        return jsonify(response)

    sql = 'SELECT email FROM users WHERE NOT user_name = %s'
    values = [req['username'], ]
    mycursor.execute(sql, values)
    result = mycursor.fetchall()
    email_list = list()
    for email in result:
        email_list.append(email[0])

    if req['password'] == "":
        sql = 'SELECT user_pass FROM users WHERE user_name = %s'
        values = [req['username'], ]
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        u_pass = result[0]
    else:
        u_pass = req['password']

    if req['email'] == "":
        sql = 'SELECT email FROM users WHERE user_name = %s'
        values = [req['username'], ]
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        u_email = result[0]
    else:
        u_email = req['email']

    if req['email'] in email_list:
        response = {
            "data": req,
            "status": False,
            "message": "This email already been used!"
        }
        return jsonify(response)

    u_phone = None if req['phone'] == "" else req['phone']
    u_role = 1 if req['role'] == "Admin" else 2

    try:
        sql = 'UPDATE users SET user_pass=%s, email=%s, phone=%s, role_id=%s ' \
              'WHERE user_name=%s'
        values = [u_pass, u_email, u_phone, u_role, req['username'], ]
        mycursor.execute(sql, values)
        mydb.commit()
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        response = {
            "data": req,
            "status": False,
            "message": f"User {req['username']} has been updated successfully!"
        }
        return jsonify(response)

def remove_user():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "username" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    try:
        sql = 'DELETE FROM users WHERE user_name=%s'
        values = [req['username'], ]
        mycursor.execute(sql, values)
        mydb.commit()
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        response = {
            "data": req,
            "status": True,
            "message": f"User {req['username']} has been removed!"
        }
        return jsonify(response)

def add_bus():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "location" not in req or "bus_name" not in req or "price" not in req \
            or "bus_type" not in req or "created_date" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    if req['bus_name'] == "" or req['price'] == "" \
            or req['bus_type'] == "" or req['location'] == "":
        response = {
            "data": req,
            "status": False,
            "message": "All field required!"
        }
        return jsonify(response)

    type_id = 1 if req['bus_type'] == "Express" else 2

    try:
        bus_list = list()
        sql = 'SELECT bus_name FROM bus'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for bus in result:
            bus_list.append(bus[0])

        if req['bus_name'] in bus_list:
            response = {
                "data": req,
                "status": False,
                "message": "Bus Name already exist"
            }
            return jsonify(response)
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)

    try:
        sql = 'SELECT loc_id FROM locations ' \
              'WHERE loc_name = %s'
        values = [req['location'], ]
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        loc_id = result[0]
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)

    try:
        sql = 'INSERT INTO bus (bus_name, loc_id, price, type_id, created_date) ' \
              'VALUES (%s,%s,%s,%s,%s)'
        values = [req['bus_name'], loc_id, float(req['price']), type_id, str(req['created_date']), ]
        mycursor.execute(sql, values)
        mydb.commit()

        sql = 'SELECT id FROM bus ORDER BY id DESC LIMIT 1'
        mycursor.execute(sql)
        result = mycursor.fetchone()
        bus_id = result[0]

        for x in range(1, 16):
            sql = 'INSERT INTO bus_seat (bus_id, seat_name) ' \
                  'VALUES (%s, %s)'
            values = [bus_id, str(x), ]
            mycursor.execute(sql, values)
            mydb.commit()
            time.sleep(0.3)

    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        response = {
            "data": req,
            "status": True,
            "message": "New Bus Added Successfully!"
        }
        return jsonify(response)

def update_bus():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "bus_id" not in req or "price" not in req or "status" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)

    if req['bus_id'] == "" or req['price'] == "" or req['status'] == "":
        response = {
            "data": req,
            "status": False,
            "message": "All field required!"
        }
        return jsonify(response)

    try:
        bus_list = list()
        sql = 'SELECT id FROM bus'
        mycursor.execute(sql)
        result = mycursor.fetchall()
        for bus in result:
            bus_list.append(bus[0])
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)

    if int(req['bus_id']) not in bus_list:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Bus ID"
        }
        return jsonify(response)

    status = 1 if req['status'] == "Active" else 0

    try:
        sql = 'UPDATE bus SET price=%s, status=%s ' \
              'WHERE id=%s '
        values = [float(req['price']), status, int(req['bus_id']), ]
        mycursor.execute(sql, values)
        mydb.commit()
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        response = {
            "data": req,
            "status": True,
            "message": "Update Successful!"
        }
        return jsonify(response)

def get_location_names():
    try:
        sql = 'SELECT loc_name FROM locations'
        mycursor.execute(sql)
    except Exception as e:
        response = {
            "data": None,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        result = mycursor.fetchall()
        locations = list()
        for location in result:
            locations.append(location[0])
        response = {
            "data": locations,
            "status": True,
            "message": "Call Success!"
        }
        return jsonify(response)

def add_trip():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "location" not in req or "bus_name" not in req \
            or "depart_date" not in req or "depart_time" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)

    created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    temp = req['depart_date'].split("-")
    temp.reverse()
    depart_date = "-".join(temp)

    depart_time = f"{depart_date} {req['depart_time']}"

    try:
        sql = 'SELECT loc_id FROM locations WHERE loc_name=%s'
        values = [req['location'], ]
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        loc_id = result[0]
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)

    try:
        sql = 'SELECT id FROM bus WHERE bus_name=%s'
        values = [req['bus_name'], ]
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        bus_id = result[0]
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)

    try:
        sql = 'INSERT INTO trip(loc_id, bus_id, departure_date, departure_time, created_at) ' \
              'VALUES (%s, %s, %s, %s, %s)'
        values = [loc_id, bus_id, depart_date, depart_time, created_date, ]
        mycursor.execute(sql, values)
        mydb.commit()

        sql = 'UPDATE bus SET status=0 ' \
              'WHERE id=%s'
        values = [bus_id, ]
        mycursor.execute(sql, values)
        mydb.commit()
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        response = {
            "data": req,
            "status": True,
            "message": "New Trip Added Successfully!"
        }
        return jsonify(response)

def update_trip():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "trip_id" not in req or "departure_date" not in req or "departure_time" not in req or "update_at" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    try:
        sql = 'UPDATE trip SET departure_date=%s, departure_time=%s, updated_at=%s ' \
              'WHERE id=%s'
        values = [req['departure_date'], req['departure_time'], req['update_at'], req['trip_id'], ]
        mycursor.execute(sql, values)
        mydb.commit()
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        response = {
            "data": req,
            "status": True,
            "message": "Trip has been updated!"
        }
        return jsonify(response)

def end_trip():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "trip_id" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    try:
        sql = 'UPDATE trip, bus, bus_seat ' \
              'SET trip.status = 0, bus.status = 1, bus_seat.status = 1 ' \
              'WHERE trip.id = %s AND trip.bus_id = bus.id AND trip.bus_id = bus_seat.bus_id'
        values = [req['trip_id'], ]
        mycursor.execute(sql, values)
        mydb.commit()
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        response = {
            "data": req,
            "status": True,
            "message": "Trip updated!"
        }
        return jsonify(response)

def get_active_trip():
    try:
        sql = 'SELECT id FROM trip WHERE status = 1'
        mycursor.execute(sql)
    except Exception as e:
        response = {
            "data": None,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        result = mycursor.fetchall()
        if not result:
            response = {
                "data": None,
                "status": True,
                "message": "No Trip Found"
            }
            return jsonify(response)
        else:
            id_list = list()
            for x in result:
                id_list.append(x[0])
            response = {
                "data": id_list,
                "status": True,
                "message": "Call Success"
            }
            return jsonify(response)

def get_active_bus():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "location" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    try:
        sql = 'SELECT loc_name FROM locations'
        mycursor.execute(sql)
    except Exception as e:
        response = {
            "data": None,
            "status": False,
            "message": f"{e}"
        }
        jsonify(response)
    else:
        location_list = list()
        result = mycursor.fetchall()
        for location in result:
            location_list.append(location[0])

        for location in location_list:
            if req['location'] == location:
                sql = 'SELECT bus.bus_name FROM bus ' \
                      'INNER JOIN locations ON bus.loc_id = locations.loc_id ' \
                      'WHERE locations.loc_name = %s AND bus.status = 1'
                values = [location, ]
                mycursor.execute(sql, values)
                result = mycursor.fetchall()
                if not result:
                    response = {
                        "data": None,
                        "status": True,
                        "message": "No Bus Available"
                    }
                    return jsonify(response)
                else:
                    bus_list = list()
                    for name in result:
                        bus_list.append(name[0])
                    response = {
                        "data": bus_list,
                        "status": True,
                        "message": "Call Success!"
                    }
                    return jsonify(response)
            elif req['location'] == "":
                sql = 'SELECT bus_name FROM bus WHERE status = 1'
                mycursor.execute(sql)
                result = mycursor.fetchall()
                if not result:
                    response = {
                        "data": None,
                        "status": True,
                        "message": "No Bus Available"
                    }
                    return jsonify(response)
                else:
                    bus_list = list()
                    for name in result:
                        bus_list.append(name[0])

                    response = {
                        "data": bus_list,
                        "status": True,
                        "message": "Call Success!"
                    }
                    return jsonify(response)

def show_user_table():
    try:
        sql = 'SELECT users.user_id, users.user_name, users.user_pass, ' \
              'users.first_name, users.last_name, users.date_of_birth, ' \
              'users.email, users.phone, role.role_name, users.status FROM users ' \
              'INNER JOIN role ON users.role_id = role.id'
        mycursor.execute(sql)
    except Exception as e:
        response = {
            "data": None,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        body = list()
        result = mycursor.fetchall()
        for data in result:
            body.append({
                "user_id": str(data[0]),
                "username": data[1],
                "password": data[2],
                "first_name": data[3] if data[3] else "None",
                "last_name": data[4] if data[4] else "None",
                "dob": str(data[5]) if data[5] else "None",
                "email": data[6] if data[6] else "None",
                "phone": data[7] if data[7] else "None",
                "role": data[8],
                "status": "Active" if data[9] == 1 else "Inactive"
            })

        response = {
            "data": body,
            "status": True,
            "message": "Call Success!"
        }
        return jsonify(response)

def show_trip_table():
    try:
        sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, ' \
              'bus.price, trip.seat, trip.departure_date, ' \
              'trip.departure_time, trip.status ' \
              'FROM trip ' \
              'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
              'INNER JOIN bus ON trip.bus_id = bus.id'
        mycursor.execute(sql)
    except Exception as e:
        response = {
            "data": None,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        body = list()
        result = mycursor.fetchall()
        if not result:
            response = {
                "data": None,
                "status": True,
                "message": "Call Success"
            }
            return jsonify(response)
        else:
            for data in result:
                body.append({
                    "trip_id": str(data[0]),
                    "bus_name": data[1],
                    "location": data[2],
                    "price": str(data[3]),
                    "seat": str(data[4]),
                    "departure_date": str(data[5]),
                    "departure_time": str(data[6]),
                    "status": "Active" if data[7] == 1 else "Inactive"
                })
            response = {
                "data": body,
                "status": True,
                "message": "Call Success!"
            }
            return jsonify(response)

def show_bus_table():
    try:
        sql = 'SELECT bus.id, bus.bus_name, bus_type.type_name, bus.bus_desc, ' \
              'bus.num_of_seat, bus.price, bus.status ' \
              'FROM bus ' \
              'INNER JOIN bus_type ON bus.type_id = bus_type.id'
        mycursor.execute(sql)
    except Exception as e:
        response = {
            "data": None,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        result = mycursor.fetchall()
        if not result:
            response = {
                "data": None,
                "status": True,
                "message": "Not found!"
            }
            return jsonify(response)
        else:
            body = list()
            for data in result:
                body.append(
                    {
                        "bus_id": str(data[0]),
                        "bus_name": data[1],
                        "bus_type": data[2],
                        "bus_desc": data[3] if data[3] else "None",
                        "seat": str(data[4]),
                        "price": str(data[5]),
                        "status": "Active" if data[6] == 1 else "Inactive"
                    }
                )
            response = {
                "data": body,
                "status": True,
                "message": "Call Success"
            }
            return jsonify(response)

def get_trip_detail():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "trip_id" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    try:
        sql = 'SELECT trip.id, bus.bus_name, locations.loc_name, trip.departure_date, trip.departure_time ' \
              'FROM trip ' \
              'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
              'INNER JOIN bus ON trip.bus_id = bus.id ' \
              'WHERE trip.id=%s'
        values = [req['trip_id'], ]
        mycursor.execute(sql, values)
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        result = mycursor.fetchone()
        body = {
            "trip_id": str(result[0]),
            "bus_name": result[1],
            "location": result[2],
            "departure_date": str(result[3]),
            "departure_time": str(result[4])
        }

        response = {
            "data": body,
            "status": True,
            "message": "Call Success"
        }
        return jsonify(response)

def get_distinct_user_id():
    uid_list = list()
    sql = 'SELECT DISTINCT user_id FROM booking'
    mycursor.execute(sql)
    result = mycursor.fetchall()
    for x in result:
        uid_list.append(x[0])
    response = {
        "data": uid_list,
        "status": True,
        "message": "Success"
    }
    return jsonify(response)

def search_transaction():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": True,
            "message": "Invalid Arguments"
        }
        return jsonify(response)

    req = request.get_json()

    booking = list()
    sql = 'SELECT id FROM booking ' \
          'WHERE user_id = %s ' \
          'ORDER BY booking_date DESC'
    values = [req['uid'], ]
    mycursor.execute(sql, values)
    result = mycursor.fetchall()
    if not result:
        response = {
            "data": None,
            "status": True,
            "message": "Not Found!"
        }
        return jsonify(response)
    else:
        data = list()
        for x in result:
            booking.append(x[0])

        # Get booking_date and price FROM booking
        for booking_id in booking:
            sql = 'SELECT booking_date, payment, status FROM booking ' \
                  'WHERE id = %s'
            values = [booking_id, ]
            mycursor.execute(sql, values)
            result = mycursor.fetchone()
            booking_date = result[0]
            price = result[1]
            paid_status = "Paid" if result[2] == 1 else "Not Paid"

            # Get seat_name FROM booking
            seat = list()
            sql = 'SELECT seat_name FROM bus_seat ' \
                  'WHERE id IN (SELECT seat_id FROM booking_detail WHERE booking_id = %s)'
            values = [booking_id, ]
            mycursor.execute(sql, values)
            result = mycursor.fetchall()
            for x in result:
                seat.append(x[0])

            # Get trip_id
            sql = 'SELECT DISTINCT trip_id FROM booking_detail ' \
                  'WHERE booking_id = %s'
            values = [booking_id, ]
            mycursor.execute(sql, values)
            result = mycursor.fetchone()
            trip_id = result[0]

            sql = 'SELECT locations.loc_name, bus.bus_name ' \
                  'FROM trip ' \
                  'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
                  'INNER JOIN bus ON trip.bus_id = bus.id ' \
                  'WHERE trip.id = %s'
            values = [trip_id, ]
            mycursor.execute(sql, values)
            result = mycursor.fetchone()
            destination = result[0]
            bus_name = result[1]

            data.append(
                {
                    "booking_id": str(booking_id),
                    "trip_id": str(trip_id),
                    "destination": destination,
                    "booking_date": str(booking_date),
                    "price": str(price),
                    "bus_name": bus_name,
                    "seat": ",".join(seat),
                    "paid_status": paid_status
                }
            )

        response = {
            "data": data,
            "status": True,
            "message": "Call Success!"
        }

        return jsonify(response)

def show_transaction():
    sql = 'SELECT id FROM booking ' \
          'ORDER BY booking_date DESC'
    mycursor.execute(sql)
    result = mycursor.fetchall()

    booking = list()
    transaction = list()
    if not result:
        response = {
            "data": None,
            "status": True,
            "message": "No Data"
        }
        return jsonify(response)
    else:
        for x in result:
            booking.append(x[0])

        for booking_id in booking:
            # Get booking_date and price from booking
            sql = 'SELECT booking_date, payment, status FROM booking ' \
                  'WHERE id = %s'
            values = [booking_id, ]
            mycursor.execute(sql, values)
            result = mycursor.fetchone()
            booking_date = result[0]
            price = result[1]
            paid_status = "Paid" if result[2] == 1 else "Not Paid"

            # Get seat_name from booking
            seat = list()
            sql = 'SELECT seat_name FROM bus_seat ' \
                  'WHERE id IN (SELECT seat_id FROM booking_detail WHERE booking_id = %s)'
            values = [booking_id, ]
            mycursor.execute(sql, values)
            result = mycursor.fetchall()
            for x in result:
                seat.append(x[0])

            # Get trip_id
            sql = 'SELECT DISTINCT trip_id FROM booking_detail ' \
                  'WHERE booking_id = %s'
            values = [booking_id, ]
            mycursor.execute(sql, values)
            result = mycursor.fetchone()
            trip_id = result[0]

            # Get destination and bus name
            sql = 'SELECT locations.loc_name, bus.bus_name ' \
                  'FROM trip ' \
                  'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
                  'INNER JOIN bus ON trip.bus_id = bus.id ' \
                  'WHERE trip.id = %s'
            values = [trip_id, ]
            mycursor.execute(sql, values)
            result = mycursor.fetchone()
            destination = result[0]
            bus_name = result[1]

            transaction.append(
                {
                    "booking_id": str(booking_id),
                    "trip_id": str(trip_id),
                    "destination": destination,
                    "booking_date": str(booking_date),
                    "price": str(price),
                    "bus_name": bus_name,
                    "seat": ",".join(seat),
                    "paid_status": paid_status,
                }
            )
        response = {
            "data": transaction,
            "status": True,
            "message": "Success",
        }
        return jsonify(response)

def show_transaction_detail():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)

    req = request.get_json()

    if "booking_id" not in req or "trip_id" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)

    sql = 'SELECT users.user_name FROM booking ' \
          'INNER JOIN users ON booking.user_id = users.user_id ' \
          'WHERE booking.id = %s'
    values = [req['booking_id'], ]
    mycursor.execute(sql, values)
    result = mycursor.fetchone()
    username = result[0]

    sql = 'SELECT locations.loc_name, trip.departure_date, trip.departure_time, bus.price ' \
          'FROM trip ' \
          'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
          'INNER JOIN bus ON trip.bus_id = bus.id ' \
          'WHERE trip.id = %s'
    values = [req['trip_id'], ]
    mycursor.execute(sql, values)
    result = mycursor.fetchone()

    data = {
        "username": username,
        "destination": result[0],
        "departure_date": str(result[1].strftime("%Y-%m-%d")),
        "unit_price": str(result[3]),
    }

    response = {
        "data": data,
        "status": True,
        "message": "Success!"
    }
    return jsonify(response)

def update_transaction():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "booking_id" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    try:
        sql = 'UPDATE booking, payment_offline ' \
              'SET booking.status = 1, payment_offline.pay_status = 1 ' \
              'WHERE booking.id = %s AND payment_offline.booking_id = %s'
        values = [req['booking_id'], req['booking_id'], ]
        mycursor.execute(sql, values)
        mydb.commit()
    except Exception as e:
        response = {
            "data": req,
            "status": False,
            "message": f"{e}"
        }
        return jsonify(response)
    else:
        response = {
            "data": req,
            "status": True,
            "message": "Transaction updated successfully!"
        }
        return jsonify(response)

def update_password():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "username" not in req or "old_pass" not in req or "new_pass" not in req or "confirm_pass" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    else:
        sql = 'SELECT user_pass FROM users WHERE user_name=%s'
        values = [req['username'], ]
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        u_pass = result[0]

        if req['old_pass'] != u_pass:
            response = {
                "data": req,
                "status": False,
                "message": "Incorrect Password"
            }
            return jsonify(response)
        if req['new_pass'] != req['confirm_pass']:
            response = {
                "data": req,
                "status": False,
                "message": "New Password and Confirm Password doesn't match"
            }
            return jsonify(response)
        try:
            sql = 'UPDATE users SET user_pass = %s WHERE user_name =%s'
            values = [req['new_pass'], req['username'], ]
            mycursor.execute(sql, values)
            mydb.commit()
        except Exception as e:
            response = {
                "data": req,
                "status": False,
                "message": f"{e}"
            }
            return jsonify(response)
        else:
            response = {
                "data": req,
                "status": True,
                "message": "Your information has been updated!"
            }
            return jsonify(response)

def update_user_info():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "username" not in req or "first_name" not in req or "last_name" not in req \
            or "phone" not in req or "email" not in req or "dob" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    else:
        try:
            sql = 'UPDATE users SET ' \
                  'first_name = %s, ' \
                  'last_name = %s, ' \
                  'phone = %s, ' \
                  'email = %s, ' \
                  'date_of_birth = %s ' \
                  'WHERE user_name = %s '
            values = [req['first_name'], req['last_name'], req['phone'],
                      req['email'], req['dob'], req['username'], ]
            mycursor.execute(sql, values)
            mydb.commit()
        except Exception as e:
            response = {
                "data": req,
                "status": False,
                "message": f"{e}"
            }
            return jsonify(response)
        else:
            response = {
                "data": req,
                "status": True,
                "message": "Success"
            }
            return jsonify(response)

def get_user_info():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "username" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    else:
        sql = 'SELECT first_name, last_name, phone, email, date_of_birth ' \
              'FROM users WHERE user_name=%s'
        values = [req['username'], ]
        mycursor.execute(sql, values)
        result = mycursor.fetchone()

        body = {
            "first_name": result[0] if result[0] else None,
            "last_name": result[1] if result[1] else None,
            "phone": result[2] if result[2] else None,
            "email": result[3] if result[3] else None,
            "dob": str(result[4].strftime("%Y-%m-%d")) if result[4] else None
        }

        response = {
            "data": body,
            "status": True,
            "message": "Success"
        }
        return jsonify(response)
