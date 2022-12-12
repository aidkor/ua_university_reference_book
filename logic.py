from SPARQLWrapper import SPARQLWrapper2, JSON
from enum import Enum


class Endpoint(Enum):
    DBPEDIA = 'http://dbpedia.org/sparql'
    WIKIDATA = 'https://query.wikidata.org/sparql'


class SPARQLConstructor:
    """
        Class for constructing query for any endpoint such as
        WIKIDATA, DBPEDIA and so on ...
    """

    def __init__(self, endpoint: Endpoint):
        self._q_history = []
        self.endpoint = endpoint
        self.sparql = SPARQLWrapper2(endpoint.value)

    # @property
    # def query(self):
    #     return self._query
    #
    # @query.setter
    # def query(self, value):
    #     self._query = value

    @property
    def q_history(self):
        return self._q_history

    def run_query(self, var_list, limit, return_format=JSON):
        self.sparql.setReturnFormat(return_format)
        self._construct_query(var_list, limit)
        self.sparql.setQuery(self.query)
        #
        # result = None
        # try:
        #     result = self.sparql.query().bindings
        #     for i in result:
        #         for j in i.keys():
        #             i[j] = i.get(j).value
        # except Exception as e:
        #     print(e)

        # self.q_history.append(self.query)
        # self.query = ''
        # return result

    def _construct_query(self, var_list, limit):
        query = ''
        # SELECT statement
        self.query += 'SELECT '
        if var_list:
            for i in var_list:
                self.query += '?' + str(i) + ' '

        # WHERE statement
        match self.endpoint:
            case Endpoint.WIKIDATA:
                self._wikidata_query()
            case Endpoint.DBPEDIA:
                self._dbpedia_query()

        # ORDER BY, GROUP BY, LIMIT
        self.query += f'LIMIT {limit}' if limit else ''

    @staticmethod
    def _select_statement():
        pass
    def _wikidata_query(self):
        self.query += 'WHERE { } '

    # TODO: add logic for dbpedia query
    def _dbpedia_query(self):
        pass


class University:
    def __init__(self, endpoint: Endpoint):
        self.sparql = SPARQLWrapper2(endpoint.value)
        # print(g.serialize(format='ttl'))

    def get_cities_data(self, limit: int = 1, c_name: bool = False, pop: bool = False):
        """ some comments """
        self.sparql.setReturnFormat(JSON)
        self.sparql.setQuery("""
           PREFIX dbr: <http://dbpedia.org/resource/>
           PREFIX dbo:  <http://dbpedia.org/ontology/>
           SELECT {c_name} {pop}
           WHERE  
           {{
                dbr:List_of_cities_in_Ukraine dbo:wikiPageWikiLink/dbo:originalName ?c_name;
                                              dbo:wikiPageWikiLink/dbo:populationTotal ?pop.
           }}
           {limit}
           """.format(
            limit={True: f'LIMIT {limit}', False: ''}[limit > 0],
            c_name={True: '?c_name', False: ''}[c_name],
            pop={True: '?pop', False: ''}[pop]))

        try:
            result = self.sparql.query().bindings
            for i in result:
                for j in i.keys():
                    i[j] = i.get(j).value

            return result

        except Exception as e:
            print(e)


if __name__ == '__main__':
    constr = SPARQLConstructor(Endpoint.WIKIDATA)
    constr.run_query(None, 0)

