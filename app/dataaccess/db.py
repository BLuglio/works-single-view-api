import psycopg2
from psycopg2.extras import RealDictCursor
import json
import settings

class DB():
    def __init__(self):
        try:
            self.conn = psycopg2.connect(host=settings.DB_HOST, port=settings.DB_PORT, 
                dbname=settings.DB_NAME, user=settings.DB_USER, password=settings.DB_PASSWORD)
            self.cur = self.conn.cursor(cursor_factory=RealDictCursor)
        except Exception as e:
            print(e)

    def executeSelectQuery(self, query):
        try:
            self.cur.execute(query)
            records = self.cur.fetchall()
            return records
        except(Exception, psycopg2.Error) as error :
            print ("Error while fetching data from PostgreSQL", error)
        finally:
            self.close()
    
    def close(self):
        self.cur.close()
        self.conn.close()