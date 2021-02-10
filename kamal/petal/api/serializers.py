from rest_framework import serializers
from petal.models import packet


class PacketSerializer(serializers.ModelSerializer):
    class Meta:
        model = packet
        fields = ['date', 'transport', 'protocol', 'conectionbytes']
