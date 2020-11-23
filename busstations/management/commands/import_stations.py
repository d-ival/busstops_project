import csv
import sys
from django.core.management.base import BaseCommand, CommandError
from busstations.models import Route, Station

class Command(BaseCommand):

    def __init__(self):
        self.known_routes = {}
        for route in Route.objects.all():
            self.known_routes[route.name] = route

        super().__init__()

    def add_arguments(self, parser):
        parser.add_argument('--f', '-filename', dest='filename', nargs='?', type=str, default='moscow_bus_stations.csv')


    def handle(self, *args, **options):
        with open(options['filename'], encoding='cp1251') as csv_file:
            reader = csv.DictReader(csv_file, delimiter=';')
            for station_data in reader:
                sys.stderr.write('Loaded: %d stations\r' % reader.line_num)
                field_values = {
                    'id': station_data['ID'],
                    'name': station_data['Name'],
                    'longitude': station_data['Longitude_WGS84'],
                    'latitude': station_data['Latitude_WGS84'],
                }

                station, created = Station.objects.update_or_create(defaults=field_values, id=station_data['ID'])
                station_routes = station_data['RouteNumbers'].split(sep=';')
                for route_num in station_routes:
                    route_num = route_num.strip()
                    if route_num in self.known_routes:
                        route = self.known_routes[route_num]
                    else:
                        route = Route.objects.create(name=route_num)
                        self.known_routes[route_num] = route
                    station.routes.add(route)



