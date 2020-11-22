from scapy.all import *
from scapy.config import conf
import subprocess
import sqlite3
conf.ipv6_enabled = False


class Network(object):
    def __init__(self):
        print("Looking for default gateway")
        prc = subprocess.Popen('route get default | grep gateway',
                               stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True)
        self.gateway = prc.communicate()
        self.gateway = self.gateway[0].decode()
        if len(self.gateway) != 0:
            self.gateway = self.gateway[4:len(self.gateway)-1].split(':')
            self.gateway = self.gateway[1][1:]
        else:
            print("Didn't found a gateway\n")
            self.gateway = input('Enter a gateway : ')

    def scan(self, timeout=20):
        self.network = []
        packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=self.gateway+'/24')
        ans, unans = srp(packet, verbose=0, timeout=timeout)
        for pkt in ans:
            self.network.append({'IP': pkt[1].psrc, 'MAC': pkt[1].hwsrc})

        return self.network

    def Echo(self, ip, count=4):
        pings = []
        for i in range(0, count):
            t = 0.0
            t1 = time.time()
            ans, unans = sr(IP(dst=ip, ttl=64)/ICMP(), verbose=0, timeout=2)
            t2 = time.time()
            t += t2-t1
            if len(ans) != 0:
                pings.append({'IP': ans[0][1].src, 'TTL': ans[0]
                              [1].ttl, 'REPLY': str((t/count)*1000)+"ms"})
            else:
                pings.append({'IP': 'Not Reachable'})
        return pings
