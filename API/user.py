from myDB import mydb, mycursor
from flask import jsonify, request

def get_location_names():
    sql = 'SELECT loc_name FROM locations'
    mycursor.execute(sql)
    location_names = mycursor.fetchall()
    data = list()
    for name in location_names:
        data.append(name)
    response = {
        "data": data,
        "status": True,
        "message": "Success"
    }
    return jsonify(response)

def check_out():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "username" not in req or "payment" not in req or "booking_date" not in req \
            or "trip_id" not in req or "price" not in req or "passenger" not in req \
            or 'seats' not in req or 'payment_method' not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    else:
        try:
            sql = 'SELECT user_id FROM users WHERE user_name = %s'
            values = [req['username'], ]
            mycursor.execute(sql, values)
            result = mycursor.fetchone()
            user_id = result[0]

            # Insert record to booking table
            sql = 'INSERT INTO booking (user_id, payment, booking_date) ' \
                  'VALUES (%s, %s, %s)'
            values = [user_id, req['payment'], req['booking_date'], ]
            mycursor.execute(sql, values)
            mydb.commit()

            # Get the last booking_id from booking table (For referencing in booking_detail later)
            sql = 'SELECT id FROM booking ORDER BY id DESC LIMIT 1'
            mycursor.execute(sql)
            result = mycursor.fetchone()
            booking_id = result[0]

            # Insert records into booking_detail
            for x in range(int(req['passenger'])):
                # Get seat_id
                sql = 'SELECT id FROM bus_seat ' \
                      'WHERE seat_name = %s AND bus_id IN ' \
                      '(SELECT bus_id FROM trip ' \
                      'WHERE id = %s)'
                values = [req['seats'][x], req['trip_id'], ]
                mycursor.execute(sql, values)
                result = mycursor.fetchone()
                seat_id = result[0]

                # Insert record to booking_detail
                sql = 'INSERT INTO booking_detail (booking_id, trip_id, seat_id, price) ' \
                      'VALUES (%s, %s, %s, %s)'
                values = [booking_id, req['trip_id'], seat_id, req['price'], ]
                mycursor.execute(sql, values)
                mydb.commit()

                # Update seat_status
                sql = 'UPDATE bus_seat SET status = 0 ' \
                      'WHERE id = %s'
                values = [seat_id, ]
                mycursor.execute(sql, values)
                mydb.commit()

                # Update trip available seat
                sql = 'UPDATE trip SET seat = seat - 1 ' \
                      'WHERE id = %s'
                values = [req['trip_id'], ]
                mycursor.execute(sql, values)
                mydb.commit()

            # Online Payment Method or Offline Payment Method
            if req['payment_method'] == "Online Payment":
                sql = 'INSERT INTO payment_online (booking_id, pay_date, cus_id) ' \
                      'VALUES (%s, %s, %s)'
                values = [booking_id, req['booking_date'], user_id, ]
                mycursor.execute(sql, values)
                mydb.commit()

                # Update Booking paid status
                sql = 'UPDATE booking SET status = 1 ' \
                      'WHERE id = %s'
                values = [booking_id, ]
                mycursor.execute(sql, values)
                mydb.commit()
            else:
                sql = 'INSERT INTO payment_offline (booking_id, booking_date, cus_id) ' \
                      'VALUES (%s, %s, %s)'
                values = [booking_id, req['booking_date'], user_id, ]
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
                "method": "Online" if req['payment_method'] == "Online Payment" else "Offline",
                "message": "Call Success"
            }
            return jsonify(response)

def search_tickets():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)

    req = request.get_json()
    if "location" not in req or "depart_date" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)

    sql = 'SELECT trip.id, trip.departure_date, trip.departure_time, trip.seat, bus.price, bus.bus_name ' \
          'FROM trip ' \
          'INNER JOIN bus ON trip.bus_id = bus.id ' \
          'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
          'WHERE trip.loc_id=(SELECT loc_id FROM locations WHERE loc_name=%s) ' \
          'AND trip.departure_date=%s AND trip.status=1'
    values = [req["location"], req["depart_date"], ]
    mycursor.execute(sql, values)
    result = mycursor.fetchall()
    count = mycursor.rowcount

    if not result:
        response = {
            "data": None,
            "status": True,
            "message": "Not Found",
            "count": count
        }
        return jsonify(response)
    else:
        body = list()
        for data in result:
            body.append(
                {
                    "trip_id": data[0],
                    "departure_date": str(data[1]),
                    "departure_time": str(data[2]),
                    "seat": data[3],
                    "price": data[4],
                    "bus_name": data[5]
                }
            )
        response = {
            "data": body,
            "status": True,
            "message": "Success",
            "count": count
        }
        return jsonify(response)

def set_trip_summary():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)

    req = request.get_json()
    if 'trip_id' not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Argument"
        }
        return jsonify(response)
    else:
        sql = 'SELECT locations.loc_name, trip.departure_date, trip.departure_time, bus.price ' \
              'FROM trip ' \
              'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
              'INNER JOIN bus ON trip.bus_id = bus.id ' \
              'WHERE trip.id=%s'
        values = [req['trip_id'], ]
        mycursor.execute(sql, values)
        data = mycursor.fetchone()
        body = {
            "location": data[0],
            "departure_date": str(data[1]),
            "departure_time": str(data[2]),
            "price": str(data[3])
        }
        response = {
            "data": body,
            "status": True,
            "message": "Call Success"
        }
        return jsonify(response)

def set_seat_layout():
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
    else:
        sql = 'SELECT seat_name, status ' \
              'FROM bus_seat ' \
              'WHERE bus_id IN (SELECT bus_id FROM trip WHERE id=%s)'
        values = [req['trip_id'], ]
        mycursor.execute(sql, values)
        result = mycursor.fetchall()
        body = list()
        for seat in result:
            body.append({
                "seat": seat[0],
                "status": True if seat[1] == 1 else False
            })
        response = {
            "data": body,
            "status": True,
            "message": "Call Success"
        }
        return jsonify(response)

def get_user_id():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()

    if 'username' not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    else:
        sql = 'SELECT user_id FROM users ' \
              'WHERE user_name = %s'
        values = [req['username'], ]
        mycursor.execute(sql, values)
        result = mycursor.fetchone()

        body = {
            "user_id": str(result[0])
        }

        response = {
            "data": body,
            "status": True,
            "message": "Call Success"
        }
        return jsonify(response)

def set_purchased_ticket():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    if "user_id" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Argument"
        }
        return jsonify(response)
    else:
        sql = 'SELECT id FROM booking WHERE user_id = %s'
        values = [req['user_id'], ]
        mycursor.execute(sql, values)
        result = mycursor.fetchall()
        booking_id_list = list()
        if not result:
            response = {
                "data": None,
                "status": True,
                "message": "No Result"
            }
            return jsonify(response)
        else:
            body = list()
            for x in result:
                booking_id_list.append(x[0])

            for booking_id in booking_id_list:
                sql = 'SELECT payment, booking_date, status FROM booking ' \
                      'WHERE id = %s'
                values = [booking_id, ]
                mycursor.execute(sql, values)
                result = mycursor.fetchone()
                price = result[0]
                booking_date = result[1]
                status = "Paid" if result[2] == 1 else "Not Paid"

                seat = list()
                sql = 'SELECT seat_name FROM bus_seat ' \
                      'WHERE id IN (SELECT seat_id FROM booking_detail WHERE booking_id = %s)'
                values = [booking_id, ]
                mycursor.execute(sql, values)
                result = mycursor.fetchall()
                for x in result:
                    seat.append(x[0])

                sql = 'SELECT DISTINCT trip_id FROM booking_detail ' \
                      'WHERE booking_id = %s'
                values = [booking_id, ]
                mycursor.execute(sql, values)
                result = mycursor.fetchone()
                trip_id = result[0]

                sql = 'SELECT locations.loc_name, bus.bus_name FROM trip ' \
                      'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
                      'INNER JOIN bus ON trip.bus_id = bus.id ' \
                      'WHERE trip.id IN (SELECT DISTINCT trip_id FROM booking_detail WHERE booking_id = %s)'
                values = [booking_id, ]
                mycursor.execute(sql, values)
                result = mycursor.fetchone()
                destination = result[0]
                bus_name = result[1]

                body.append({
                    "booking_id": str(booking_id),
                    "trip_id": str(trip_id),
                    "destination": destination,
                    "booking_date": str(booking_date),
                    "price": str(price),
                    "bus_name": str(bus_name),
                    "seat": ",".join(seat),
                    "paid_status": status
                })

            response = {
                "data": body,
                "status": True,
                "message": "Call Success"
            }
            return jsonify(response)

            # booking_id = str(booking_id),
            # trip_id = str(trip_id),
            # destination = destination,
            # booking_date = str(booking_date),
            # price = str(price),
            # bus_name = bus_name,
            # seat = ",".join(seat),
            # paid_status = paid_status,

def get_purchase_summary():
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
    else:
        sql = 'SELECT locations.loc_name, trip.departure_date, trip.departure_time, bus.price ' \
              'FROM trip ' \
              'INNER JOIN locations ON trip.loc_id = locations.loc_id ' \
              'INNER JOIN bus ON trip.bus_id = bus.id ' \
              'WHERE trip.id=%s'
        values = [req['trip_id'], ]
        mycursor.execute(sql, values)
        result = mycursor.fetchone()
        body = {
            "location": result[0],
            "departure_date": str(result[1]),
            "departure_time": str(result[2]),
            "price": str(result[3])
        }
        response = {
            "data": body,
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

    sql = 'SELECT first_name, last_name, phone, email, date_of_birth FROM users ' \
          'WHERE user_name = %s'
    values = [req['username'], ]
    mycursor.execute(sql, values)
    result = mycursor.fetchone()

    body = {
        "first_name": result[0],
        "last_name": result[1],
        "phone": result[2],
        "email": result[3],
        "dob": result[4].strftime("%Y-%m-%d")
    }
    response = {
        "data": body,
        "status": True,
        "message": "Success"
    }
    return jsonify(response)

def update_user_password():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)

    req = request.get_json()
    if "username" not in req or "password" not in req \
            or "new_pass" not in req or "confirm_pass" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)

    sql = 'SELECT user_pass FROM users ' \
          'WHERE user_name = %s'
    values = [req['username'], ]
    mycursor.execute(sql, values)
    result = mycursor.fetchone()

    if req['password'] != result[0]:
        response = {
            "data": req,
            "status": False,
            "message": "Incorrect Password"
        }
        return jsonify(response)
    else:
        if req['new_pass'] != req['confirm_pass']:
            response = {
                "data": req,
                "status": False,
                "message": "Confirm password does not match with new password"
            }
            return jsonify(response)
        else:
            try:
                sql = 'UPDATE users SET ' \
                        'user_pass = %s ' \
                        'WHERE user_name = %s'
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
                    "message": "Your password has been updated!"
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
    if "username" not in req or "first_name" not in req \
            or "last_name" not in req or "email" not in req \
            or "phone" not in req or "dob" not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)

    email_list = list()
    sql = 'SELECT email FROM users ' \
          'WHERE NOT user_name = %s'
    values = [req['username'], ]
    mycursor.execute(sql, values)
    result = mycursor.fetchall()
    for email in result:
        email_list.append(email[0])

    if req['email'] in email_list:
        response = {
            "data": req,
            "status": False,
            "message": "This email already taken"
        }
        return jsonify(response)

    try:
        sql = 'UPDATE users SET ' \
              'first_name = %s, last_name = %s, email = %s, phone = %s, date_of_birth = %s ' \
              'WHERE user_name = %s'
        values = [req['first_name'], req['last_name'], req['email'], req['phone'], req['dob'], req['username'], ]
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
