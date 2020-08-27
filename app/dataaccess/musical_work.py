
from . import db

def get_by_iswc(iswc):
    query = f"SELECT iswc, title, array_agg(contributor) as contributors FROM musical_work WHERE iswc='{iswc}' GROUP BY iswc, title"
    result = db.DB(host="localhost", port=5432, database="bmat", user="postgres", password="postgres").executeSelectQuery(query)
    return result

def get_all():
    query = f"SELECT iswc, title, array_agg(contributor) as contributors FROM musical_work GROUP BY iswc, title"
    result = db.DB(host="localhost", port=5432, database="bmat", user="postgres", password="postgres").executeSelectQuery(query)
    return result

# def get_musical_work_csv(iswc):
#     query = f"SELECT iswc, title, contributor FROM musical_work WHERE iswc='{iswc}'"
#     tuples = db.DB(host="localhost", port=5432, database="bmat", user="postgres", password="postgres").executeSelectQuery(query)
#     print(tuples)
#     return tuples