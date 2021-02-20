from elasticsearch import Elasticsearch

es = Elasticsearch(HOST="http://localhost", PORT=9200)


def hits():
    body = {
        "from": 0,
        "query": {
            "match": {
                "network.protocol": "dns"
            }
        }
    }
    res = es.search(index='packetbeat-7.10.2-2021.01.25-000001', body=body)
    return res['hits']['total']['value']


def alertDNS(hit):
    body = {
        "from": 0,
        "size": hit,
        "query": {
            "match": {
                "network.protocol": "dns"
            }
        }
    }
    res = es.search(index='packetbeat-7.10.2-2021.01.25-000001', body=body)

    return res['hits']['hits']


class DomainNameServer:
    COUNT = 0

    def dns(self):
        while True:
            count = hits()
            if count != self.COUNT:
                packet = alertDNS(count)
                for i in range(self.COUNT, count-1):
                    self.classifier(packet[i])
                self.COUNT = count
            break

    def classifier(self, pkt):
        url = pkt['_source']['resource']
        try:
            ip = pkt['_source']['resolved_ip']
        except:
            ip = None
        with open('../blacklist.kamal', 'r') as f:
            blacklist = f.read()
        if url in blacklist:
            pass


obj = DomainNameServer()
obj.dns()
