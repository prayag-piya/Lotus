from elasticsearch import Elasticsearch
import datetime
es = Elasticsearch(['localhost:9200'])


def index():
    year = datetime.datetime.today().year
    month = datetime.datetime.today().month
    day = datetime.datetime.today().day
    if day < 10:
        day = ".0"+str(day)
    if month < 10:
        month = ".0"+str(month)

    concat_index = str(year) + str(month)+str(day)
    return f'packetbeat-7.12.0-{concat_index}'


DOCUMENT_INDEX = index()


def totalHits():
    count = es.count(index=DOCUMENT_INDEX)
    return count['count']


def parsing(hits):
    count = totalHits()
    req = es.search(index=DOCUMENT_INDEX, body={'size': count['count']})
    return req['hits']['hits']
