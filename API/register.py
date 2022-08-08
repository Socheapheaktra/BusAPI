from myDB import mydb, mycursor
from flask import request, jsonify
from datetime import datetime

def register_user():
    sql = 'SELECT user_name, email FROM users'
    mycursor.execute(sql)
    username_list = list()
    email_list = list()
    result = mycursor.fetchall()
    if not result:
        pass
    else:
        for user in result:
            username_list.append(user[0])
            email_list.append(user[1])
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Argument"
        }
        return jsonify(response)
    req = request.get_json()
    if 'username' not in req or 'password' not in req or 'email' not in req:
        response = {
            "data": req,
            "status": False,
            "message": "Bad Request"
        }
        return jsonify(response)
    if req['username'] in username_list:
        response = {
            "data": req,
            "status": False,
            "message": "This username has been taken"
        }
        return jsonify(response)
    elif req['email'] in email_list:
        response = {
            "data": req,
            "status": False,
            "message": "This email has been taken"
        }
        return jsonify(response)
    else:
        try:
            created_date = datetime.now().strftime("%Y-%m-%d")
            sql = 'INSERT INTO users(user_name, user_pass, email, created_date) ' \
                  'VALUES (%s, %s, %s, %s)'
            values = [req['username'], req['password'], req['email'], created_date, ]
            mycursor.execute(sql, values)
            mydb.commit()
        except Exception as e:
            response = {
                "data": req,
                "status": False,
                "message": f"{e.args[0]}"
            }
            return jsonify(response)
        else:

            response = {
                "data": req,
                "status": True,
                "message": "Your account has been created!"
            }
            return jsonify(response)
