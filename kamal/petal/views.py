from django.shortcuts import render
from django.views.generic import *
from .models import *
import json
from network.scanner import *
# Create your views here.


class index(View):
    template_name = "petal/index.html"
    content = {}

    def get(self, request):
        data = ''
        dataset = {}
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
        self.content['dataset'] = json.dumps(dataset)
        print(json.dumps(dataset))
        return render(request, self.template_name, self.content)
