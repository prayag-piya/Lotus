from django.shortcuts import render
from django.views.generic import *
from .models import *
import json
from .utlis import *
import threading
# Create your views here.


class index(View):
    template_name = "petal/index.html"
    content = {}

    def get(self, request):
        data = ''
        dataset = {}
        hst = host.objects.all()
        pkt = packet.objects.all()

        for i in pkt:
            dateT = str(i.date).split(' ')
            if dateT[0] not in data:
                data += dateT[0]+','
            if dateT[0] not in dataset.keys():
                dataset[dateT[0]] = [i.conectionbytes]
            else:
                dataset[dateT[0]].append(i.conectionbytes)

        self.content['data'] = data
        self.content['host'] = hst
        self.content['dataset'] = json.dumps(dataset)
        return render(request, self.template_name, self.content)


class dns(View):
    template_name = 'petal/domain.html'
    content = {}

    def get(self, request):
        return render(request, self.template_name, self.content)
