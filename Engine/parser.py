import requests
import json


def totalHits():
    req = requests.get('http://127.0.0.1:9200/packetbeat-7.10.2/_search')
    resp = req.content
    dict_resp = json.loads(resp)
    return dict_resp['hits']['total']['value']


def parsing(hits):
    req = requests.get(
        'http://127.0.0.1:9200/packetbeat-7.10.2/_search?size='+str(hits))
    resp = req.content
    dict_resp = json.loads(resp)
    return dict_resp['hits']['hits']
