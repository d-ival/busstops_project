from django.db import models


class Station(models.Model):

    latitude = models.FloatField()
    longitude = models.FloatField()
    routes = models.ManyToManyField('Route', related_name='stations')
    name = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.name} ({self.longitude}, {self.latitude})"

    def route_numbers(self):
        return ", ".join(map(str, self.routes.all()))


class Route(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def center(self):
        stations = Station.objects.filter(routes=self)
        center_y = stations.aggregate(avg_latitude=models.Avg('latitude'))
        center_x = stations.aggregate(avg_longitude=models.Avg('longitude'))
        return {
            'x': center_x['avg_longitude'],
            'y': center_y['avg_latitude']
        }
