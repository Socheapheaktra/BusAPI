import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="",
    database="bus_reservation"
)

mycursor = mydb.cursor()
