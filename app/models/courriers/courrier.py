from app.models.baseModel import BaseModel
from app.models.courriers.constants import COURRIERS
from app.models.courriers.errors import CourrierNotFound
from app.models.packages.package import Package


class Courrier(BaseModel):
    def __init__(self, name, service_type=None, _id=None):
        super().__init__(_id)
        self.name = name
        self.service_type = service_type

    @staticmethod
    def find_courrier(data: dict):
        from app.models.courriers.aeroflash.aeroflash import Aeroflash
        courrier_names = data.get('courrier_name')
        courrier: Courrier = None
        if courrier_names in COURRIERS:
            if courrier_names == "Aeroflash":
                courrier = Aeroflash(**data)
            elif courrier_names == "Estafeta":
                pass
            elif courrier_names == "DHL":
                pass
            else:
                raise CourrierNotFound(
                    f"El courrier seleccionado no existe, confirme que mando que correcto, courrier_name: {courrier_names}")
        return courrier

    def find_prices(self, package: Package) -> float or tuple:
        pass

    def find_delivery_day(self):
        pass