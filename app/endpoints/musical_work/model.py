from dataaccess import db

class MusicalWork():
    __tablename__ = 'works_single_view'
    db = db.DB()

    def get_by_iswc(self, iswc):
        query = f"SELECT id, iswc, title, contributors FROM {self.__tablename__} WHERE iswc='{iswc}'"
        result = self.db.execute_select_query(query)
        return result

    def get_all(self):
        query = f"SELECT id, iswc FROM {self.__tablename__}"
        result = self.db.execute_select_query(query)
        return result

    # def __repr__(self):
    #     return 'id: {}, ISWC: {}, contributor: {}, title: {}'.format(self.id, self.iswc, self.contributor, self.title)