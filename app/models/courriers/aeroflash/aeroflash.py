import datetime

from app import Database
from app.models.courriers.aeroflash.constants import AREAS_COLLECTION, AREA_TO_ZONE_COLLECTION, ZONE_TO_RATE, \
    TYPE_KG_LIMIT, DELIVERY_TIME
from app.models.courriers.courrier import Courrier
from app.models.courriers.dhl.constants import TYPES
from app.models.courriers.errors import ZipCodesNotFound, CourrierServiceTypeUnkown
from app.models.packages.package import Package


class Aeroflash(Courrier):

    def find_prices(self, package: Package) -> dict:
        self.set_type()
        result = dict()
        if isinstance(self.type, list):
            for service_type in self.type:
                result[service_type] = self.find_type_price(service_type, package)
        else:
            result[self.type] = self.find_type_price(self.type, package)
        return result

    @classmethod
    def find_type_price(cls, service_type: str, package: Package) -> float:
        """
        given a service type it starts to calculate the price of the shipment
        :param service_type:  str of service type
        :param package:  PAckage detail
        :return: float containing the price
        """
        if service_type not in TYPE_KG_LIMIT:
            raise CourrierServiceTypeUnkown(
                f'El tipo ({service_type}) de servicio seleccionado para {cls.__name__} no existe')
        area_from, area_to = Aeroflash.find_area(package)
        zone = Aeroflash.find_zone(area_from, area_to)
        return cls.find_rate(service_type, zone, package)

    @staticmethod
    def find_area(package: Package) -> (int, int):
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
    def find_zone(area_from: int, area_to: int) -> int:
        """
        given the areas from which they are sending and receiving it gets the zone to which the rate will be
        calculates
        :param area_from:
        :param area_to:
        :return:
        """
        zone = Database.find(AREA_TO_ZONE_COLLECTION, {'x': area_from, 'y': area_to}).next()
        return zone['value']

    @staticmethod
    def find_rate(service_type: str, zone: int, package: Package) -> float:
        """
        After obtaining the zone, it finds the rate it needs and calculates the prices of the shipment
        even if it haves an exceeded weight it calculates it.
        :param service_type: str of service type to calculate
        :param zone: int of the calculated zone
        :param package: Package detail
        :return: float of shipment price
        """
        exceeded_price = 0
        if package.weight % 1 > 0:
            package_weight = int(package.weight) + 1  # if it has more than an int weight it must add 1
        else:
            package_weight = int(package.weight)
        # finds the exceeded weight and rate, with that it calculates the exceeded price
        if TYPE_KG_LIMIT[service_type] < package_weight:
            exceeded_weight = package_weight - TYPE_KG_LIMIT[service_type]
            package_weight = TYPE_KG_LIMIT[service_type]
            exceeded_query = {'type': service_type, 'rates_by_zone.zone': zone, 'rates_by_zone.kg': '+'}
            exceeded_project = {'_id': 0, 'rates_by_zone': {'$elemMatch': {'zone': zone, 'kg': '+'}},
                                'rates_by_zone.rate': 1}
            exceeded_rate = Database.find(ZONE_TO_RATE, exceeded_query, exceeded_project).next()['rates_by_zone'][0][
                'rate']
            exceeded_price = exceeded_rate * exceeded_weight

        query = {'type': service_type, 'rates_by_zone.zone': zone, 'rates_by_zone.kg': package_weight}
        project = {'_id': 0, 'rates_by_zone': {'$elemMatch': {'zone': zone, 'kg': package_weight}},
                   'rates_by_zone.rate': 1}
        rate = Database.find(ZONE_TO_RATE, query, project).next()['rates_by_zone'][0]['rate']
        return rate + exceeded_price

    def find_delivery_day(self) -> str:
        today = datetime.datetime.now()
        delivery_day = today + datetime.timedelta(**DELIVERY_TIME)

        return delivery_day.strftime("%Y-%m-%d")

    def set_type(self)->None:
        if self.type is None:
            self.type = TYPES