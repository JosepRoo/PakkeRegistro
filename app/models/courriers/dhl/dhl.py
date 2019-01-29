import datetime

from app import Database
from app.models.courriers.courrier import Courrier
from app.models.courriers.dhl.constants import TYPE_KG_LIMIT, AREAS_COLLECTION, ZONE_TO_RATE, DELIVERY_TIME, TYPES
from app.models.courriers.dhl.constants import MAX_WEIGHT, GAS_RATE
from app.models.courriers.errors import CourrierServiceTypeUnkown, ZipCodesNotFound
from app.models.packages.package import Package


class DHL(Courrier):
    max_weight = MAX_WEIGHT

    def find_prices(self, package: Package) -> dict:
        self.set_type()
        if self.type not in TYPE_KG_LIMIT:
            raise CourrierServiceTypeUnkown(
                f'El tipo ({self.type}) de servicio seleccionado para {self.__class__.__name__} no existe')
        # DHL.is_available(package)
        return {self.type: self.find_rate(package)}

    @staticmethod
    def is_available(package: Package) -> (dict, dict):
        try:
            area_from = Database.find(AREAS_COLLECTION, {'zip_codes': package.origin_zipcode}).next()
            area_to = Database.find(AREAS_COLLECTION, {'zip_codes': package.destiny_zipcode}).next()
        except StopIteration:
            raise ZipCodesNotFound("No Hay Disponibilidad")

        return area_from, area_to

    def find_rate(self, package) -> float:
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
        if TYPE_KG_LIMIT[self.type] < package_weight:
            exceeded_weight = package_weight - TYPE_KG_LIMIT[self.type]
            package_weight = TYPE_KG_LIMIT[self.type]
            exceeded_query = {'type': self.type, 'rates.kg': '+'}
            exceeded_project = {'_id': 0, 'rates': {'$elemMatch': {'kg': '+'}},
                                'rates.rate': 1}
            exceeded_rate = Database.find(ZONE_TO_RATE, exceeded_query, exceeded_project).next()['rates'][0][
                'rate']
            exceeded_price = exceeded_rate * exceeded_weight

        query = {'type': self.type, 'rates.kg': package_weight}
        project = {'_id': 0, 'rates': {'$elemMatch': {'kg': package_weight}},
                   'rates.rate': 1}
        rate = Database.find(ZONE_TO_RATE, query, project).next()['rates'][0]['rate']
        extra_fees = self._get_extra_fees(package)
        return round((rate + exceeded_price + extra_fees) * GAS_RATE, 2)

    def _get_extra_fees(self, package: Package) ->float:
        ext_zone = list(Database.find('DHL_EXT', {"_id": package.destiny_zipcode}))
        extra_fees = 0
        if ext_zone:
            extra_fees += 133.67

        if package.weight > 70.0:
            extra_fees += 244.90

        if package.width > 120 or package.length > 120 or package.height > 120:
            extra_fees += 244.90

        return extra_fees


    def find_delivery_day(self) -> str:
        today = datetime.datetime.now()
        delivery_day = today + datetime.timedelta(**DELIVERY_TIME)

        return delivery_day.strftime("%Y-%m-%d")

    def set_type(self) -> None:
        if self.type is None:
            self.type = TYPES
        elif isinstance(self.type, list):
            self.type = self.type[0]
