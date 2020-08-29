import pandas as pd
import numpy as np


class Processor():

    # extract all iswc codes from a pandas data frame, filtering out null values and duplicates
    # @returns: list of iswc codes
    def extract_iswcs(self, df):
        df_clean = df.drop_duplicates().dropna()
        return list(df_clean["iswc"])
    
    # extract all the contributors for a given iswc, eliminating the duplicate values
    # @params: dataset, indices to consider, list of partial results
    # @returns: list of strings 
    def extract_contributors(self, data, indices, contributors_list):
        if len(indices) == 0:
            single_contributors = set()
            for c in contributors_list:
                _list = c.split("|")
                for elem in _list:
                    single_contributors.add(elem)
            return list(single_contributors)
        else:
            idx = indices.pop()
            cur_row = data[idx]
            contributors_list.append(cur_row[2])
            return self.extract_contributors(data, indices, contributors_list) 
    
    def compose_query(self, iswc, contributors, title):
        return f"INSERT INTO musical_work_test (iswc, contributors, title, source) VALUES ('{iswc}', ARRAY{contributors}, '{title}') ON CONFLICT DO UPDATE SET contributors=ARRAY{contributors};"

    def process(self, filepath):
        _file = pd.read_csv(filepath)
        ### data pre processing: ###
        #   1) filter columns
        #   2) take all iswcs without duplicates and discard the rows with a null iswc
        #   3) for each iswc extract the contributors
        data = pd.DataFrame(_file, columns=['iswc', 'title', 'contributors']).values.tolist()
        df = pd.DataFrame(_file, columns=['iswc'])
        iswcs = self.extract_iswcs(df)
        result = []
        for iswc in iswcs:
            # indici delle occorrenze del brano corrente in data
            indices = [i for i, x in enumerate(data) if x[0] == iswc]
            title = data[indices[0]][1]
            if(pd.isnull(title)):
                title = ''
            contributors = self.extract_contributors(data, indices, [])
            result.append({'iswc': iswc, 'title': title, 'contributors': contributors})
        return result