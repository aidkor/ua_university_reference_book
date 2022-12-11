from SPARQLWrapper import SPARQLWrapper2, JSON
from rdflib import Graph, Namespace
from enum import Enum


class Endpoint(Enum):
    DBPEDIA = 'http://dbpedia.org/sparql'
    WIKIDATA = 'https://query.wikidata.org/sparql'


class SPARQLConstructor:
    """
        General class for managing, retrieving and store data from any endpoint
    """

    @staticmethod
    def create_query(*args, **kwargs):
        pass


class University:
    def __init__(self, endpoint: Endpoint):
        self.endpoint = endpoint
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
    print(City().get_cities_data(True, True))

