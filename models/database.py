import os
import MySQLdb
from dotenv import load_dotenv

class Database:

    def __init__(self):
        load_dotenv()
        self.host =  os.environ['HOST']
        self.port =  os.environ['PORT']
        self.user_name =  os.environ['USER_NAME']
        self.password =  os.environ['PASSWORD']
        self.db_name =  os.environ['DB_NAME']

        self.connection = MySQLdb.connect(
            user=self.user_name, 
            password=self.password,
            host=self.host,
            database=self.db_name)           
        self.cursor = self.connection.cursor()


    def select(self, query):
        self.cursor.execute(query)
        fetchall = self.cursor.fetchall()


        return fetchall
    
    def insert_data(self, query):
        try:
            self.cursor.execute(query)
            self.connection.commit()

            lastrowid = self.cursor.lastrowid
            return lastrowid
        except Exception as e:
            print(e)
            return 0

    def close(self):
        self.connection.close()
