from django.shortcuts import render
from django.views.generic import *
# Create your views here.


class index(View):
    template_name = "petal/index.html"

    def get(self, request):
        return render(request, self.template_name, {})
