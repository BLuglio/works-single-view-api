import psycopg2
from psycopg2.extras import RealDictCursor
import json

class DB():
    def __init__(self, host, port, database, user, password):
        try:
            self.conn = psycopg2.connect(host=host, port=port, 
                dbname=database, user=user, password=password)
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