from django.db import models


class host(models.Model):
    name = models.CharField(max_length=100)
    os = models.CharField(max_length=100)
    kernel = models.CharField(max_length=100)
    ipaddrs = models.CharField(max_length=100)
    mac = models.CharField(max_length=100)
    service = models.CharField(max_length=200)


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
