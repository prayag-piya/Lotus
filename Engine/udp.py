import joblib
from elasticsearch import Elasticsearch
import datetime
from parser import DOCUMENT_INDEX


class UDP(object):
    def __init__(self):
        self.es = Elasticsearch('localhost:9200')

    def classify(self, packet, protocol):
        self.packet = packet

        if protocol == 'dns':
            self.DomainNameServer()
            self.udpRFC()

    def DomainNameServer(self):
        file = open('/Users/prayagpiya/Desktop/Lotus/blacklist.kamal', 'r')
        data = file.read()
        data = data.split('\n')
        if self.packet['_source']['dns']['answers'][0]['name'] in data:
            print('Alert')

    def udpRFC(self):
        # duration spkts dpkts sbytes dbytes rate sttl dttl sload sloss dloss sinpkt dinpkt sjit djit
        '''
        dur
spkts
dpkts
sbytes
dbytes
rate
sttl
dttl
sload
dload
sloss
dloss
sinpkt
dinpkt
sjit
djit
swin
stcpb
dtcpb
dwin
tcprtt
synack
ackdat
smean
dmean
trans_depth
response_body_len
ct_srv_src
ct_state_ttl
ct_dst_ltm
ct_src_dport_ltm
ct_dst_sport_ltm
ct_dst_src_ltm
is_ftp_login
ct_ftp_cmd
ct_flw_http_mthd
ct_src_ltm
ct_srv_dst
is_sm_ips_ports
proto_3pc
proto_a/n
proto_aes-sp3-d
proto_any
proto_argus
proto_aris
proto_arp
proto_ax.25
proto_bbn-rcc
proto_bna
proto_br-sat-mon
proto_cbt
proto_cftp
proto_chaos
proto_compaq-peer
proto_cphb
proto_cpnx
proto_crtp
proto_crudp
proto_dcn
proto_ddp
proto_ddx
proto_dgp
proto_egp
proto_eigrp
proto_emcon
proto_encap
proto_etherip
proto_fc
proto_fire
proto_ggp
proto_gmtp
proto_gre
proto_hmp
proto_i-nlsp
proto_iatp
proto_ib
proto_icmp
proto_idpr
proto_idpr-cmtp
proto_idrp
proto_ifmp
proto_igmp
proto_igp
proto_il
proto_ip
proto_ipcomp
proto_ipcv
proto_ipip
proto_iplt
proto_ipnip
proto_ippc
proto_ipv6
proto_ipv6-frag
proto_ipv6-no
proto_ipv6-opts
proto_ipv6-route
proto_ipx-n-ip
proto_irtp
proto_isis
proto_iso-ip
proto_iso-tp4
proto_kryptolan
proto_l2tp
proto_larp
proto_leaf-1
proto_leaf-2
proto_merit-inp
proto_mfe-nsp
proto_mhrp
proto_micp
proto_mobile
proto_mtp
proto_mux
proto_narp
proto_netblt
proto_nsfnet-igp
proto_nvp
proto_ospf
proto_pgm
proto_pim
proto_pipe
proto_pnni
proto_pri-enc
proto_prm
proto_ptp
proto_pup
proto_pvp
proto_qnx
proto_rdp
proto_rsvp
proto_rtp
proto_rvd
proto_sat-expak
proto_sat-mon
proto_sccopmce
proto_scps
proto_sctp
proto_sdrp
proto_secure-vmtp
proto_sep
proto_skip
proto_sm
proto_smp
proto_snp
proto_sprite-rpc
proto_sps
proto_srp
proto_st2
proto_stp
proto_sun-nd
proto_swipe
proto_tcf
proto_tcp
proto_tlsp
proto_tp++
proto_trunk-1
proto_trunk-2
proto_ttp
proto_udp
proto_unas
proto_uti
proto_vines
proto_visa
proto_vmtp
proto_vrrp
proto_wb-expak
proto_wb-mon
proto_wsn
proto_xnet
proto_xns-idp
proto_xtp
proto_zero
service_None
service_dhcp
service_dns
service_ftp
service_ftp-data
service_http
service_irc
service_pop3
service_radius
service_smtp
service_snmp
service_ssh
service_ssl
state_ACC
state_CLO
state_CON
state_ECO
state_FIN
state_INT
state_PAR
state_REQ
state_RST
state_URN
state_no
        '''
        dbody = {
            'query': {
                'match': {
                    'destination.ip': self.packet['_source']['destination']['ip']
                }
            }
        }
        sbody = {
            'query': {
                'match': {
                    'source.ip': self.packet['_source']['source']['ip']
                }
            }
        }
        dpkts = self.es.count(index=DOCUMENT_INDEX, body=dbody)
        dpkts = dpkts['count']
        spkts = self.es.count(index=DOCUMENT_INDEX, body=sbody)
        spkts = spkts['count']
        byts = self.packet['_source']['network']['bytes']
        duration = self.packet['_source']['event']['duration']
        try:
            sbytes = self.packet['_source']['source']['bytes']
        except:
            sbytes = 0
        try:
            dbytes = self.packet['_source']['destination']['bytes']
        except:
            dbytes = 0
        time =


# from elasticsearch import Elasticsearch

# es = Elasticsearch(HOST="http://localhost", PORT=9200)


# def hits():
#     body = {
#         "from": 0,
#         "query": {
#             "match": {
#                 "network.protocol": "dns"
#             }
#         }
#     }
#     res = es.search(index='packetbeat-7.12.07.10.2-2021.01.25', body=body)
#     return res['hits']['total']['value']


# def alertDNS(hit):
#     body = {
#         "from": 0,
#         "size": hit,
#         "query": {
#             "match": {
#                 "network.protocol": "dns"
#             }
#         }
#     }
#     res = es.search(index='packetbeat-7.12.07.10.2-2021.01.25', body=body)

#     return res['hits']['hits']


# class DomainNameServer:
#     COUNT = 0

#     def dns(self):
#         while True:
#             count = hits()
#             if count != self.COUNT:
#                 packet = alertDNS(count)
#                 for i in range(self.COUNT, count-1):
#                     self.classifier(packet[i])
#                 self.COUNT = count
#             break

#     def classifier(self, pkt):
#         url = pkt['_source']['resource']
#         try:
#             ip = pkt['_source']['resolved_ip']
#         except:
#             ip = None
#         with open('../blacklist.kamal', 'r') as f:
#             blacklist = f.read()
#         if url in blacklist:
#             pass


# obj = DomainNameServer()
# obj.dns()
