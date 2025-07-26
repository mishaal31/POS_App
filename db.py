import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="127.0.0.1",
        user="root",          
        password="mishtuf",           
        database="pos_system"
    )