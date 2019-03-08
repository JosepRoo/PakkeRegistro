import datetime
import requests
from requests import Timeout

from app.models.courriers.courrier import Courrier
from app.models.courriers.errors import CourrierErrors
from app.models.courriers.noventaynueveminutos.constants import TYPES, URL, USER_ID, API_KEY, QRO_ZIP_CODE, MAX_WEIGHT
from app.models.courriers.noventaynueveminutos.errors import NoventaYNueveMinutosError
from app.models.packages.package import Package


class NoventaYNueveMinutos(Courrier):
    max_weight = MAX_WEIGHT

    def find_prices(self, package: Package) -> dict:
        """
        given a list or str of courrier types it will get the prices for each one
        :param package: Package detail
        :return: dict for each service to calculate with the price as value
        """
        if package.destiny_zipcode in QRO_ZIP_CODE:
            raise NoventaYNueveMinutosError("Queretaro no esta habilitado por el momento")
        self.set_type()
        result = dict()
        data = {
            "apiKey": API_KEY,
            "userId": USER_ID,
            "weight": package.weight,
            "width": package.width,
            "height": package.height,
            "depth": package.length,
            "destination": {"postalCode": package.destiny_zipcode, "country": "Mexico"},
            "origin": {"postalCode": package.origin_zipcode, "country": "Mexico"}
        }
        headers = {"Content-Type": "application/json"}
        try:
            res = requests.post(URL, json=data, headers=headers, timeout=5)
        except Timeout:
            raise CourrierErrors("99m no respondió")
        res = res.json()
        if res['status'] == "Error":
            raise NoventaYNueveMinutosError(res['message'])
        res = res['rates']
        for service_type in self.type:
            if service_type not in TYPES:
                result[service_type] = f"El servicio de tipo: {service_type} no es una opcion valida"
            for rate in res:
                if '99' in service_type and rate['type'] == '99':
                    if rate['vehicle'] in service_type:
                        result[service_type] = rate['cost']
                        break
                elif rate['vehicle'] == service_type and rate['type'] != '99':
                    result[service_type] = rate['cost']
                    break
            if result.get(service_type) is None:
                result[service_type] = "Error, para los CPs dados no hay cobertura"
        return result

    def find_delivery_day(self) -> str:
        """
        given the courrier, depending on each one it will calculate the day estimated of completed delivery
        :return: str with datetime data
        """
        return datetime.datetime.now().strftime("%Y-%m-%d")

    def set_type(self) -> None:
        """sets the type of the courrier if it wasn't set at __init__"""
        if self.type is None:
            self.type = list(TYPES)
        elif not isinstance(self.type, list):
            self.type = [self.type]
