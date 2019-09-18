import os

from app.models.courriers.courrier import Courrier
from app.models.courriers.errors import CourrierErrors
from app.models.packages.package import Package
from zeep import Client


class RedPack(Courrier):
    url = os.environ.get("REDPACK_WSDL")
    pin = os.environ.get("REDPACK_PIN")
    user_id = os.environ.get("REDPACK_ID")
    client = Client(url)
    max_weight = 150

    def find_prices(self, package: Package) -> dict:
        guide = {
            "remitente": {
                "codigoPostal": package.origin_zipcode,
                "pais": "Mexico"
            },
            "consignatario": {
                "codigoPostal": package.destiny_zipcode,
                "pais": "Mexico"
            },
            "paquetes": [
                {
                    "largo": int(round(package.length, 0)),
                    "ancho": int(round(package.width)),
                    "alto": int(round(package.height)),
                    "peso": int(round(package.weight))
                }
            ],
            "tipoEntrega": {
                "equivalencia": "DOM",
                "descripcion": "Domicilio"
            },
            "flag": 2,
            "tipoEnvio": {
                "id": "2"
            }
        }   
        try:
            result = self.client.service.cotizacionNacional(PIN=self.pin, idUsuario=self.user_id, guias=[guide])[0]
        except Exception as e:
            raise CourrierErrors("The RedPack Service answered with error:" + str(e))
            
        try:
            services = dict()
            for rate in result.cotizaciones:
                options = {det.descripcion: det.costoBase for det in rate.detallesCotizacion}
                services[rate.tipoServicio.descripcion] = {"price": rate.tarifa,
                                                        "options": options,
                                                        'delivery_day': rate.tiempoEntrega.strftime("%Y-%m-%d")}

            return services
        except Exception as e:
            raise CourrierErrors("The RedPack Service answered with error:" + str(e))
