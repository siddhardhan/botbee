import pandas as pd 
import pyodbc
import os
import pandas.io.sql as psql
from config import DefaultConfig
from user_details import UserDetails


CONFIG = DefaultConfig()
conn_str = "DRIVER={};SERVER=tcp:{};PORT=1433;DATABASE={};UID={};PWD={}".format(
    CONFIG.SQL_DRIVER, 
    CONFIG.SQL_DB_SERVER,
    CONFIG.SQL_DATABASE,
    CONFIG.SQL_USERNAME,
    os.getenv('SQL_PASSWORD') )

def addUser(user: UserDetails):
    if getUser(user.email_id).size == 0:
        with pyodbc.connect(conn_str) as conn:
            with conn.cursor() as cursor:
                query = "INSERT INTO Users VALUES ('{}', '{}', '{}', '{}')".format(user.email_id, user.role, user.experience, user.level)
                cursor.execute(query)
                conn.commit()

def getUser(email_id: str):
    with pyodbc.connect(conn_str) as conn:
        with conn.cursor() as cursor:
            query = "SELECT * FROM Users WHERE EMAIL_ID='{}'".format(email_id)
            df = psql.read_sql(query, conn)
            
            df= df.rename(columns=str.lower)
            print(df)
    return df

