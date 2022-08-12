import mysql.connector

'''
For cloud

host="b5grqlbaqnhiu3xs5zqs-mysql.services.clever-cloud.com"
user="umirqrxz6pdfjjpo"
passwd="4Lj01OwXEH0e5t7ZKIFU"
port="3306"
database="b5grqlbaqnhiu3xs5zqs"

For local
host="localhost"
user="root"
passwd=""
database="bus_reservation"
'''


"""For Using Cloud"""
mydb = mysql.connector.connect(
    host="b5grqlbaqnhiu3xs5zqs-mysql.services.clever-cloud.com",
    user="umirqrxz6pdfjjpo",
    passwd="4Lj01OwXEH0e5t7ZKIFU",
    database="b5grqlbaqnhiu3xs5zqs"
)

"""For Using Local"""
# mydb = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     passwd="",
#     database="bus_reservation"
# )

mycursor = mydb.cursor()
