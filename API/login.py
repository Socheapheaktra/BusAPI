from myDB import mycursor
from flask import request, jsonify

def validate_user():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Arguments"
        }
        return jsonify(response)
    req = request.get_json()
    sql = 'SELECT users.user_name, users.user_pass, role.role_name, users.status ' \
          'FROM users ' \
          'INNER JOIN role ON users.role_id = role.id'
    mycursor.execute(sql)
    users = mycursor.fetchall()
    if not users:
        response = {
            "data": None,
            "status": False,
            "message": "No data"
        }
        return jsonify(response)
    else:
        user_list = list()
        for username in users:
            user_list.append(username[0])

        if req['username'] not in user_list:
            response = {
                "data": req,
                "status": False,
                "message": "Invalid Username"
            }
            return jsonify(response)
        else:
            for user in users:
                if req['username'] == user[0]:
                    if req['password'] == user[1]:
                        body = {
                            "username": user[0],
                            "password": user[1],
                            "role": user[2],
                            "status": user[3]
                        }
                        response = {
                            "data": req if user[3] == 0 else body,
                            "status": False if user[3] == 0 else True,
                            "message": "Account Blocked!" if user[3] == 0 else "Success!"
                        }
                        return jsonify(response)
                    else:
                        response = {
                            "data": req,
                            "status": False,
                            "message": "Incorrect Password"
                        }
                        return jsonify(response)
