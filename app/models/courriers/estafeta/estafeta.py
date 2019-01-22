import datetime

from app import Database
from app.models.courriers.courrier import Courrier
from app.models.courriers.errors import CourrierServiceTypeUnkown, CourrierErrors
from app.models.courriers.estafeta.constants import create_graph, EXTRA_FEE, SPECIAL_TYPE, TYPE_KG_LIMIT, \
    TYPES_STR_TO_ID, TYPES_ID_TO_STR, DF_ZIP_CODES, TYPES_ID_TOSERVICE_TYPE
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
        self.discard_types(package)
        result = dict()
        if isinstance(self.type, list):
            for service_type in self.type:
                result[TYPES_ID_TO_STR[service_type]] = self.find_type_price(service_type, package)
                result[TYPES_ID_TO_STR[service_type]]['delivery_day'] = self.find_delivery_day(package)
        else:
            result[TYPES_ID_TO_STR[self.type]] = self.find_type_price(self.type, package)
        return result

    def discard_types(self, package):
        option_types = list(Database.find("Estafeta_cities", {"zip_code": package.destiny_zipcode}))
        terrain_flag = False
        for opt in option_types:
            if opt['service_type'] == 'TERRESTRE':
                terrain_flag = True
                break
        if not option_types or not terrain_flag:
            option_types += [{
                'zip_code': package.destiny_zipcode,
                'periodicity': 'SEMANAL',
                'extra': 1,
                'service_type': 'TERRESTRE',
                'availability': [1, 1, 1, 1, 1, 0, 0]

            }]
        result = list()
        if isinstance(self.type, list):
            for type in self.type:
                for opt_type in option_types:
                    if TYPES_ID_TOSERVICE_TYPE.get(opt_type['service_type']) == type:
                        result.append(type)
                        continue
        self.type = result

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
        try:
            return Database.find("Estafeta_cities", {"zip_code": package.destiny_zipcode}).next()
        except StopIteration:
            not_found_dict = {
                'zip_code': package.destiny_zipcode,
                'periodicity': 'SEMANAL',
                'extra': 1,
                'service_type': 'TERRESTRE',
                'availability': [1, 1, 1, 1, 1, 0, 0]

            }
            return not_found_dict
            # raise CourrierErrors(
            #     CourrierErrorsf"El Codigo Postal {package.destiny_zipcode} no esta disponible para envios con este Courrier")

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
        if (package.origin_zipcode in DF_ZIP_CODES and package.destiny_zipcode in DF_ZIP_CODES) and service_type != \
                TYPES_STR_TO_ID['ESTAFETA_DIA_SIGUIENTE']:
            service_type = "8608731"
        if service_type == SPECIAL_TYPE:
            price, descriptions = cls.Graph.dijkstra(0, package_weight)
            result_descriptions = dict()
            for description in descriptions:
                if result_descriptions.get(description) is None:
                    result_descriptions[description] = 1
                    if "TERRESTRE" in description:
                        result_descriptions["cuenta"] = list(Database.find("Estafeta_rates", {"type": description}))[0][
                            '_id']
                else:
                    result_descriptions[description] += 1

            return {"price": price, "options": result_descriptions}
        rate = Database.find("Estafeta_rates", {"_id": service_type}).next()
        exceeded_price = 0
        exceeded_weight = 0
        if package_weight > rate['kg']:
            exceeded_weight = package_weight - rate['kg']
            exceeded_price = rate['adicional'] * exceeded_weight

        final_rate = rate['total'] + exceeded_price
        options = {rate['type']: 1, 'adicional': exceeded_weight, "cuenta": service_type}
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
