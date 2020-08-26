
from . import db

def get_musical_work(iswc):
    query = f"SELECT iswc, title, array_agg(contributor) as contributors FROM musical_work WHERE iswc='{iswc}' GROUP BY iswc, title"
    tuples = db.DB(host="localhost", port=5432, database="bmat", user="postgres", password="postgres").executeSelectQuery(query)
    return tuples