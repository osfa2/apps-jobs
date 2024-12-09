import os
import MySQLdb
from dotenv import load_dotenv

class Database:

    def __init__(self):
        load_dotenv()
        host =  os.environ['HOST']
        port =  os.environ['PORT']
        user_name =  os.environ['USER_NAME']
        password =  os.environ['PASSWORD']
        db_name =  os.environ['DB_NAME']

        self.connection = MySQLdb.connect(
            user=user_name, 
            password=password,
            host=host,
            database=db_name)           
        self.cursor = self.connection.cursor()


    def select(self, query):
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def insert_data(self, query):
        self.cursor.execute(query)
        self.connection.commit()
        return self.cursor.lastrowid

    def close(self):
        self.connection.close()
