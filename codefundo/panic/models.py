from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class PanicLocation(models.Model):

    account = models.ForeignKey('Account', on_delete=models.CASCADE)
    lat = models.DecimalField(default=0, max_digits=15, decimal_places=10)
    lng = models.DecimalField(default=0, max_digits=15, decimal_places=10)
    time = models.DateTimeField(auto_now=True)


class Location(models.Model):

    account = models.OneToOneField('Account', on_delete=models.CASCADE)
    lat = models.DecimalField(default=0, max_digits=15, decimal_places=10)
    lng = models.DecimalField(default=0, max_digits=15, decimal_places=10)
    time = models.DateTimeField(auto_now=True)


class Account(models.Model):

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    first_name = models.CharField(max_length=100, null=True)
    country = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return '{0}, {1}'.format(self.last_name, self.first_name)


class DisasterArea(models.Model):

    lat = models.IntegerField(default=0)
    lng = models.IntegerField(default=0)
    disaster_type = models.CharField(max_length=100, null=True)

    def __str__(self):
        return 'Disaster at- lat:{0} lng:{1}'.format(self.lat, self.lng)

