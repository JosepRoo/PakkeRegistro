import datetime

from app import Database
from app.models.courriers.courrier import Courrier
from app.models.courriers.errors import CourrierServiceTypeUnkown
from app.models.courriers.estafeta.constants import create_graph, EXTRA_FEE, SPECIAL_TYPE, TYPE_KG_LIMIT, \
    TYPES_STR_TO_ID
from app.models.packages.package import Package


class Estafeta(Courrier):
    Graph = create_graph()

    def set_type(self) -> None:
        if self.type is None:
            self.type = [v for k, v in TYPES_STR_TO_ID.items()]
        elif isinstance(self.type, list):
            try:
                temp_list = list()
                for serv_type in self.type:
                    temp = serv_type
                    temp_list.append(TYPES_STR_TO_ID[temp])
                self.type = temp_list
            except KeyError:
                raise CourrierServiceTypeUnkown(
                    f'El tipo ({temp}) de servicio seleccionado para {self.__class__.__name__} no existe')
        else:
            try:
                temp = self.type
                self.type = TYPES_STR_TO_ID[self.type]
            except KeyError:
                raise CourrierServiceTypeUnkown(
                    f'El tipo ({temp}) de servicio seleccionado para {self.__class__.__name__} no existe')

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
    def find_type_price(cls, service_type: str, package: Package) -> dict:
        """
        given a service type it starts to calculate the price of the shipment
        :param service_type:  str of service type
        :param package:  Package detail
        :return: float containing the price
        """
        delivery_data = cls.find_delivery_data(package)
        extra_fee = EXTRA_FEE if delivery_data['extra'] == 1 else 0
        rate = cls.find_rate(service_type, package)
        rate['price'] += extra_fee
        rate['options']['extra_fee'] = extra_fee

        return rate

    @staticmethod
    def find_delivery_data(package: Package) -> dict:
        return Database.find("Estafeta_cities", {"zip_code": package.destiny_zipcode}).next()

    # def determine_searches(self) -> None:
    #     non_optimizable_types = {service_type for service_type in self.type if service_type in NON_OPTIMIZABLE_TYPES}
    #     optimizable_types = {service_type for service_type in self.type if service_type in OPTIMIZABLE_TYPES}
    #     if len(optimizable_types) >= 5:
    #         self.type = list(non_optimizable_types | SPECIAL_TYPE)

    @classmethod
    def find_rate(cls, service_type: str, package: Package) -> dict:
        if package.weight % 1 > 0:
            package_weight = int(package.weight) + 1  # if it has more than an int weight it must add 1
        else:
            package_weight = int(package.weight)
        if package_weight >= TYPE_KG_LIMIT and service_type == SPECIAL_TYPE:
            service_type = "5522411"
        if service_type == SPECIAL_TYPE:
            price, descriptions = cls.Graph.dijkstra(0, package_weight)
            result_descriptions = dict()
            for description in descriptions:
                if result_descriptions.get(description) is None:
                    result_descriptions[description] = 1
                else:
                    print("lol")
                    result_descriptions[description] += 1

            return {"price": price, "options": result_descriptions}
        rate = Database.find("Estafeta_rates", {"_id": service_type}).next()
        exceeded_price = 0
        exceeded_weight = 0
        if package_weight > rate['kg']:
            exceeded_weight = package_weight - rate['kg']
            exceeded_price = rate['adicional'] * exceeded_weight

        final_rate = rate['total'] + exceeded_price
        options = {rate['type']: 1, 'adicional': exceeded_weight}
        return {'price': final_rate, "options": options}

    def find_delivery_day(self, package: Package) -> str:
        today = datetime.datetime.now()
        weekday = today.weekday()
        delivery_data = self.find_delivery_data(package)
        if delivery_data['periodicity'] == "DIARIA":
            days = 2 if weekday == 5 else 1
            delivery_day = today + datetime.timedelta(days=days)
        else:
            days = 5 - weekday if weekday <= 5 else 6
            for day in delivery_data['availability'][weekday:] + delivery_data['availability'][:weekday]:
                days += 1
                if day == 1:
                    break

            delivery_day = today + datetime.timedelta(days=days)
        return delivery_day.strftime("%Y-%m-%d")
