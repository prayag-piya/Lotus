from django.shortcuts import render, redirect
from django.views.generic import *
from .models import *
import json
from .utlis import *
import threading
from django.contrib import messages
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

    def post(self, request):
        pass


class dns(View):
    template_name = 'petal/domain.html'
    content = {}

    def get(self, request):
        return render(request, self.template_name, self.content)


class plan(View):
    template_name = 'petal/plan.html'
    content = {}

    def get(self, request):
        return render(request, self.template_name, self.content)

    def post(self, request):
        thresshold = request.POST['thresshold']
        try:
            thresshold = int(thresshold)
            ipaddrs = request.POST['ipaddrs']
            port = int(request.POST['port'])
            data = open(
                '/Users/prayagpiya/Desktop/Lotus/kamal/package.json', 'r')
            data = data.read()
            jsonData = json.loads(data)
            srvobj = ddosplan.objects.all()
            print(len(srvobj))
            if jsonData['ddos_plan'] <= len(srvobj):
                messages.error(request, 'You have already subcribe')
                return render(request, self.template_name, self.content)
            else:
                obj = ddosplan(thresshold=thresshold,
                               ipaddrs=ipaddrs, service=port)
                obj.save()
                return redirect('/network/')
        except:
            messages.error(
                request, 'Pls enter valid inforatiom')
            return render(request, self.template_name, self.content)


class rules(View):
    template_name = 'petal/rules.html'
    content = {}

    def get(self, request):
        file = open('/Users/prayagpiya/Desktop/Lotus/blacklist.kamal', 'r')
        filedata = file.read()
        filedata = filedata.split('\n')
        if len(filedata) == 1:
            filedata = []
        self.content['blacklist'] = filedata
        return render(request, self.template_name, self.content)

    def post(self, request):
        filedata = handlePost(request)
        self.content['blacklist'] = filedata

        return redirect('/rules/')


class network(View):
    template_name = "petal/network.html"
    content = {}

    def get(self, request):
        obj = ddosplan.objects.all()
        self.content['objects'] = obj
        return render(request, self.template_name, self.content)

    def post(self, request):

        return redirect('/network/')
