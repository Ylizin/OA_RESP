from elasticsearch import Elasticsearch
import random
es = Elasticsearch()

DSL = {\
    'query': {'match': {'content': ''}}, 
    'size': 20, 
    'sort': [{'_score': 'desc'}, 
    {'author_stars': 'desc'}, 
    {'star': 'desc'}]
    }

def query_es(query_str):
    DSL['query']['match']['content'] = query_str
    res = es.search(index='poems',body=DSL)['hits']['hits']
    if not res:
        return None
    idx = random.randint(0,len(res)-1)

    return res[idx]['_source']['content']
    # return '\n'.join([r['_source']['content'] for r in res])