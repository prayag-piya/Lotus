from parser import es
import datetime
import sqlite3
import multiprocessing
import time


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


class Thresshold(object):
    CONSUMED_BANDWIDTH = 0.0
    WORKING_HOUR = True
    flow_id = []

    def __init__(self, databaseobj):
        #self.host = '192.168.1.101'
        self.host = databaseobj[2]
        self.service = databaseobj[3]
        self.THRESSHOLD = databaseobj[1]
        self.HITS = 0

    def totalHits(self):
        self.size = 0
        self.destination_body = {
            'size': self.size,
            'query': {
                'multi_match': {
                    'query': self.host,
                    'fields': ['destination.ip', 'source.ip']
                }
            },
        }
        self.destination_size = es.search(
            index=index(), body=self.destination_body)
        self.size = self.destination_size['hits']['total']['value']
        return self.size

    def packets(self):
        body = {
            'size': self.totalHits(),
            'query': {
                'multi_match': {
                    'query': self.host,
                    'fields': ['destination.ip', 'source.ip']
                }
            },
        }
        self.destination_data = es.search(
            index=index(), body=body)
        return self.destination_data['hits']['hits']

    def ddos_mitigation(self):
        while True:
            if int(time.localtime()[3]) >= 9 and int(time.localtime()[3]) <= 18:
                self.WORKING_HOUR = True
            else:
                self.WORKING_HOUR = False
            hit = self.totalHits()
            if hit != self.HITS:
                data = self.packets()
                for i in range(self.HITS, hit-1):
                    self.classification(data[i])
                self.HITS = hit
            if self.WORKING_HOUR:
                time.sleep(300)
            else:
                time.sleep(600)

    def alert(self):
        consumed = self.THRESSHOLD * (80/100)
        if consumed == self.CONSUMED_BANDWIDTH:
            print("Your network consumsion is about to reach your thresshold")

    def classification(self, data):
        if data['_source']['type'] == 'flow':
            unique = data['_source']['flow']['id']
            if data['_source']['flow']['final'] == False:
                if unique not in self.flow_id:
                    self.flow_id.append(unique)
                    into_gb = data['_source']['network']['bytes'] / 1073741824
                    self.CONSUMED_BANDWIDTH += into_gb
                else:
                    into_gb = data['_source']['network']['bytes'] / 1073741824
                    self.CONSUMED_BANDWIDTH += into_gb
            else:
                body = {
                    'query': {
                        'match': {
                            'flow.id': {
                                'query': unique,
                            }
                        }
                    }
                }
                final_byts = 0
                value = es.search(index=DOCUMENT_INDEX, body=body)
                value = value['hits']['total']['value']
                body['size'] = value
                final = es.search(index=DOCUMENT_INDEX, body=body)
                for i in final['hits']['hits']:
                    into_gb = i['_source']['network']['bytes'] / 1073741824
                    final_byts += into_gb

                self.CONSUMED_BANDWIDTH -= final_byts

        elif data['_source']['type'] != 'tls':
            into_gb = data['_source']['network']['bytes'] / 1073741824
            self.CONSUMED_BANDWIDTH += into_gb
        print(self.CONSUMED_BANDWIDTH)

        self.alert()


t1 = time.time()
con = sqlite3.connect('/Users/prayagpiya/Desktop/Lotus/kamal/db.sqlite3')
cur = con.cursor()
plans = cur.execute('select * from petal_ddosplan')
processes = []
for plan in plans:
    thress = Thresshold(plan)
    process = multiprocessing.Process(target=thress.ddos_mitigation)
    process.start()
    processes.append(process)

for process in processes:
    process.join()
print(time.time()-t1)
