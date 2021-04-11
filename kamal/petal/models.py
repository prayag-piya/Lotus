from django.db import models


class host(models.Model):
    state = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    ipaddrs = models.CharField(max_length=100)
    mac = models.CharField(max_length=100)
    service = models.CharField(max_length=200)

    def __str__(self):
        return self.os


class packet(models.Model):
    CHOICES = (
        ('tls', 'Transport Layer Security'),
        ('http', 'Hypertext Transport Protocol'),
        ('dns', 'Domain Name Service'),
        ('uc', 'Uncatogoried'),
    )
    date = models.DateTimeField(unique=True)
    transport = models.CharField(max_length=10)
    protocol = models.CharField(max_length=10, choices=CHOICES)
    conectionbytes = models.IntegerField()

    def __str__(self):
        return self.protocol


class ddosplan(models.Model):
    thresshold = models.IntegerField()
    ipaddrs = models.CharField(max_length=100)
    service = models.IntegerField()

    def __str__(self):
        return self.ipaddrs + ' ---- ' + str(self.thresshold)
