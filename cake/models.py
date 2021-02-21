from django.db import models
from django.contrib.auth import models as auth
from django.conf import settings as djangoSettings
from django.utils.html import mark_safe
#from django.contrib.postgres.fields import JSONField

class Forecast(models.Model):
    email = models.EmailField('Inhaber', default='bakeryforecastlog@gmail.com')
    #ttl = models.DateTimeField('Lebensdauer')
    link = models.URLField('Link nach Vorhersage', default='No link')

    @classmethod
    def create(cls, *params):
        instance = cls(params)
        return instance

    def __str__(self):
        return self.link

class Chart(models.Model):

    class ChartType(models.TextChoices):
        CLUSTER = 'CL', ('Cluster')
        PAIRS = 'PR', ('Pairs') 
        FORECAST = 'FR', ('Forecast')

    date_from = models.TextField(default='2020-12-1') #models.DateTimeField('YearMonth', default='')
    date_to = models.TextField(default='2020-12-1')
    option = models.CharField(max_length=2, choices=ChartType.choices, default=ChartType.CLUSTER)
    json = models.TextField(default='')
    branch = models.IntegerField(default=0)
    #json = JSONField()

    def __str__(self):
        return self.json 

class Visual(models.Model):
    user = models.ForeignKey(auth.User, on_delete=models.CASCADE)
    path = models.URLField('Link nach file')
    pic = models.ImageField('Abbildung', upload_to='plotly_db')

    def picture(self):
        return mark_safe("<img src=string>"%self.path)

    def __str__(self):
        return self.path
