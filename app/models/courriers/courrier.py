from app.models.baseModel import BaseModel
from app.models.courriers.constants import COURRIERS, set_html
from app.models.courriers.errors import CourrierNotFound
from app.models.packages.package import Package


class Courrier(BaseModel):
    def __init__(self, name, type=None, _id=None):
        super().__init__(_id)
        self.name = name
        self.type = type

    @staticmethod
    def find_courrier(data: dict):
        """
        given the data of the request it gets what courrier will be calculating the price
        :param data: dict containing the services and name of courrier
        :return: Courrier with the data
        """
        from app.models.courriers.aeroflash.aeroflash import Aeroflash
        from app.models.courriers.dhl.dhl import DHL
        from app.models.courriers.estafeta.estafeta import Estafeta
        from app.models.courriers.noventaynueveminutos.noventaynueveminutos import NoventaYNueveMinutos
        from app.models.courriers.fedex.Fedex import Fedex

        name = data.get('name')
        courrier: Courrier = None
        if name in COURRIERS:
            if name == "AEF":
                courrier = Aeroflash(**data)
            elif name == "STF":
                courrier = Estafeta(**data)
            elif name == "DHL":
                courrier = DHL(**data)
            elif name == "99Minutos":
                courrier = NoventaYNueveMinutos(**data)
            elif name == "FDX":
                courrier = Fedex(**data)
        else:
            raise CourrierNotFound(
                f"El courrier seleccionado no existe, confirme que mando que correcto, name: {name}")
        return courrier

    def find_prices(self, package: Package) -> dict:
        """
        given a list or str of courrier types it will get the prices for each one
        :param package: Package detail
        :return: dict for each service to calculate with the price as value
        """
        pass

    def find_delivery_day(self) -> str:
        """
        given the courrier, depending on each one it will calculate the day estimated of completed delivery
        :return: str with datetime data
        """
        pass

    def set_type(self) -> None:
        """sets the type of the courrier if it wasn't set at __init__"""
        pass
