from django.db import models

class Client(models.Model):
    username = models.CharField(max_length=100, unique=True)

class Deal(models.Model):
    customer = models.ForeignKey(Client, related_name='deals', on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    date = models.DateTimeField()
    gems = models.ManyToManyField('Gem', related_name='deals')


class Gem(models.Model):
    name = models.CharField(max_length=100)


