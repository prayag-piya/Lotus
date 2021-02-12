from parser import totalHits, parsing
import threading
import sqlite3
import requests
import time


class kamal(object):
    HITS = 0

    def packets(self):
        while True:
            hit = totalHits()
            if hit != self.HITS:
                reqpacket = parsing(hit)
                for i in range(self.HITS, hit-1):
                    self.Classifier(reqpacket[i])
                self.HITS = hit
            break

    def Classifier(self, process):
        try:
            if process['_source']['network']['transport'] == 'tcp':
                try:
                    date = process['_source']['@timestamp']
                    trasport = 'tcp'
                    try:
                        protocol = process['_source']['network']['protocol']
                    except:
                        protocol = 'Uncatogoried'
                    byts = process['_source']['network']['bytes']
                except:
                    byts = 0
            elif process['_source']['network']['transport'] == 'udp':
                try:
                    date = process['_source']['@timestamp']
                    trasport = 'udp'
                    try:
                        protocol = process['_source']['network']['protocol']
                    except:
                        protocol = 'Uncatogoried'
                    byts = process['_source']['network']['bytes']
                except:
                    byts = 0
            elif process['_source']['network']['transport'] == 'icmp':
                print('icmp')
            elif process['_source']['network']['transport'] == 'arp':
                print('arp')
            else:
                print('We dont have following classfier')
            self.trafficCount(date, trasport, protocol, byts)
        except:
            date = process['_source']['@timestamp']
            protocol = 'uc'
            trasport = 'uc'
            byts = 0
            self.trafficCount(date, trasport, protocol, byts)

    def trafficCount(self, timestamp, trasp, port, bytes_bytes):
        # obj = packet(timestamp=timestamp, transport=trasp,
        #              portocol=port, connectionbytes=bytes_bytes)
        # obj.save()
        try:
            content = {'date': timestamp, 'transport': trasp,
                       'protocol': port, 'conectionbytes': bytes_bytes}
            req = requests.post(
                'http://127.0.0.1:8000/api/packet/packetview/', data=content)
        except Exception as e:
            print(e)


obj = kamal()
obj.packets()