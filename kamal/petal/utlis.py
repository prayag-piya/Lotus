from django.contrib import messages
import json


def handlePost(request):
    try:
        data = json.loads(request.body)
        name = data['name']
        file = open('/Users/prayagpiya/Desktop/Lotus/blacklist.kamal', 'r')
        filedata = file.read()
        filedata = filedata.split('\n')
        filedata.remove(name)
        f = open('/Users/prayagpiya/Desktop/Lotus/blacklist.kamal', 'w')
        filep = '\n'.join(filedata)
        f.write(filep)
    except:
        file = open('/Users/prayagpiya/Desktop/Lotus/blacklist.kamal', 'r')
        filedata = file.read()
        filedata = filedata.split('\n')
        data = request.POST['blacklist']
        file = open('/Users/prayagpiya/Desktop/Lotus/blacklist.kamal', 'a')
        if data in filedata:
            messages.info(
                request, 'Request already in the list')
        else:
            messages.info(
                request, 'Request added sccessfully')
            file.write('\n'+data)

    return filedata
