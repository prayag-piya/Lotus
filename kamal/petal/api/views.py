from django.core import serializers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from petal.models import *
from petal.api.serializers import *


@api_view(['GET', 'POST'])
def api_packet(request):
    if request.method == 'GET':
        pkt = packet.objects.all()
        serializer = PacketSerializer(pkt, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = PacketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def api_host(request):
    if request.method == 'GET':
        hst = host.objects.all()
        serializer = HostSerializer(hst, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = HostSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
