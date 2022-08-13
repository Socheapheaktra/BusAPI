from myDB import mydb, mycursor
from flask import jsonify, request

def get_people():
    try:
        sql = 'SELECT * FROM test'
        mycursor.execute(sql)
    except Exception as err:
        response = {
            "data": None,
            "status": False,
            "message": f"{err}"
        }
        return jsonify(response)
    else:
        body = list()
        result = mycursor.fetchall()
        for people in result:
            body.append(
                {
                    "id": str(people[0]),
                    "first_name": people[1],
                    "last_name": people[2],
                    "gender": people[3],
                    "country": people[4]
                }
            )
        response = {
            "data": body,
            "status": True,
            "message": "Success!"
        }
        return jsonify(response)

def add_people():
    if not request.data or not request.is_json:
        response = {
            "data": None,
            "status": False,
            "message": "Invalid Data"
        }
        return jsonify(response)
    req = request.get_json()
    try:
        sql = 'INSERT INTO test(first_name, last_name, gender, country) ' \
              'VALUES (%s, %s, %s, %s)'
        values = [req['first_name'], req['last_name'], req['gender'], req['country'],]
        mycursor.execute(sql, values)
        mydb.commit()
    except Exception as err:
        response = {
            "data": req,
            "status": False,
            "message": f"{err}"
        }
        return jsonify(response)
    else:
        response = {
            "data": req,
            "status": True,
            "message": "Success"
        }
        return jsonify(response)