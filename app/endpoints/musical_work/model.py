from dataaccess import db

class MusicalWork():
    __tablename__ = 'works_single_view'
    __single_view_obj__ = {"iswc", "title", "contributors"}
    db = db.DB()

    def get_by_iswc(self, iswc):
        query = f"SELECT id, iswc, title, contributors, cast (created_at as timestamp(0)), cast (modified_at as timestamp(0)) FROM {self.__tablename__} WHERE iswc='{iswc}'"
        result = self.db.execute_select_query(query)
        return result

    def get_all(self):
        query = f"SELECT id, iswc FROM {self.__tablename__}"
        result = self.db.execute_select_query(query)
        return result
    
    # insert [{'iswc':...,'title':...,'contributors':[...]}] 
    def insert(self, _list):
        try:
            query = "BEGIN;\n"
            for elem in _list:
                if self.__single_view_obj__ <= elem.keys():
                    iswc = elem['iswc']
                    title = elem['title']
                    contributors = elem['contributors']
                    query += f"INSERT INTO {self.__tablename__} (iswc, contributors, title, created_at) VALUES ('{iswc}', ARRAY{contributors}, '{title}', now()) ON CONFLICT ON CONSTRAINT iswc DO UPDATE SET contributors=ARRAY{contributors}, modified_at=now();\n"
                else:
                    return False
            query += "COMMIT;"
            result = self.db.execute_insert_query(query)
            return result
        except(Exception) as error:
            print(error)