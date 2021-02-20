from rest_framework import serializers
from petal.models import *


class PacketSerializer(serializers.ModelSerializer):
    class Meta:
        model = packet
        fields = ['date', 'transport', 'protocol', 'conectionbytes']


class HostSerializer(serializers.ModelSerializer):
    class Meta:
        model = host
        fields = ['state', 'os', 'ipaddrs', 'mac', 'service']
