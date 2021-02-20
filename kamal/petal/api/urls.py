from django.urls import path
from petal.api.views import *

app_name = 'petal'

urlpatterns = [
    path('packetview/', api_packet, name='packet'),
    path('hostview/', api_host, name='host')
]
