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
        packet = Ether(dst='ff:ff:ff:ff:ff:ff')/ARP(pdst=self.gateway+'/24')/Padding(
            load='\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00')
        ans, unans = srp(packet, verbose=0, timeout=timeout)
        print(ans)
        for pkt in ans:
            self.network.append({'IP': pkt[1].psrc, 'MAC': pkt[1].hwsrc})

        return self.network


obj = Network()
print(obj.scan())
