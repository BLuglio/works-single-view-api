import psycopg2
from psycopg2.extras import RealDictCursor
import json
import settings

class DB():
    def __open_connection__(self):
        try:
            self.conn = psycopg2.connect(host=settings.DB_HOST, port=settings.DB_PORT, 
                dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD)
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(e)

    def execute_select_query(self, query):
        try:
            self.__open_connection__()
            self.cur.execute(query)
            records = self.cur.fetchall()
            return records
        except(Exception, psycopg2.Error) as error :
            print ("Error while fetching data from PostgreSQL", error)
        finally:
            self.__close_connection__()
    
    def __close_connection__(self):
        self.cur.close()
        self.conn.close()