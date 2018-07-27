import datetime

from app import Database
from app.models.courriers.aeroflash.constants import AREAS_COLLECTION, AREA_TO_ZONE_COLLECTION, ZONE_TO_RATE, \
    TYPE_KG_LIMIT, DELIVERY_TIME
from app.models.courriers.courrier import Courrier
from app.models.courriers.errors import ZipCodesNotFound, CourrierServiceTypeUnkown
from app.models.packages.package import Package


class Aeroflash(Courrier):

    def find_prices(self, package: Package):
        if self.service_type not in TYPE_KG_LIMIT.keys():
            raise CourrierServiceTypeUnkown(
                f'El tipo ({self.service_type})de servicio seleccionado para {self.__class__.__name__} no existe')
        area_from, area_to = Aeroflash.find_area(package)
        zone = Aeroflash.find_zone(area_from, area_to)
        self.find_rate(zone, package)

    @staticmethod
    def find_area(package: Package) -> tuple:
        """
        Given the package it determines the area of the destiny zipcode and the origin zipcode
        :param package: Package
        :return: tuple of areas
        """
        try:
            area_from = Database.find(AREAS_COLLECTION, {'zip_codes': package.origin_zipcode}).next()['Area']
            area_to = Database.find(AREAS_COLLECTION, {'zip_codes': package.destiny_zipcode}).next()['Area']
        except StopIteration:
            raise ZipCodesNotFound("No Hay Disponibilidad")

        return area_from, area_to

    @staticmethod
    def find_zone(area_from, area_to) -> float:
        zone = Database.find(AREA_TO_ZONE_COLLECTION, {'x': area_from, 'y': area_to}).next()
        return zone

    def find_rate(self, zone: float, package: Package) -> float:
        exceeded_price = 0
        if TYPE_KG_LIMIT[self.service_type] > package.weight:
            exceeded_weight = package.weight - TYPE_KG_LIMIT[self.service_type]
            package.weight = TYPE_KG_LIMIT[self.service_type]
            exceeded_query = {'type': self.service_type, 'rates_by_zone.zone': zone, 'rates_by_zone.kg': '+'}
            exceeded_project = {'_id': 0, 'rates_by_zone': {'$elemMatch': {'zone': zone, 'kg': '+'}},
                                'rates_by_zone.rate': 1}
            exceeded_rate = Database.find(ZONE_TO_RATE, exceeded_query, exceeded_project).next()['rates_by_zone'][0][
                'rate']
            exceeded_price = exceeded_rate * exceeded_weight

        query = {'type': self.service_type, 'rates_by_zone.zone': zone, 'rates_by_zone.kg': package.weight}
        project = {'_id': 0, 'rates_by_zone': {'$elemMatch': {'zone': zone, 'kg': package.weight}},
                   'rates_by_zone.rate': 1}
        rate = Database.find(ZONE_TO_RATE, query, project)

        return rate + exceeded_price

    def find_delivery_day(self):
        today = datetime.datetime.now()
        delivery_day = today + datetime.timedelta(DELIVERY_TIME)

        return delivery_day.strftime("%Y-%m-%d")
