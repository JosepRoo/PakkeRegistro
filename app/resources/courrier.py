from operator import itemgetter

from flask_restful import Resource, reqparse

from app import Response
from app.common.utils import Utils
from app.models.courriers.courrier import Courrier as CourrierModel
from app.models.courriers.constants import COURRIERS
from app.models.courriers.errors import CourrierErrors
from app.models.packages.package import Package as PackageModel


class Courrier(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('pakke_key',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )
    parser.add_argument('courrier_services',
                        type=dict,
                        required=True,
                        help="This field cannot be blank.",
                        action='append',
                        location='json'
                        )
    parser.add_argument('weight',
                        type=float,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )
    parser.add_argument('width',
                        type=float,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )
    parser.add_argument('length',
                        type=float,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )
    parser.add_argument('height',
                        type=float,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )
    parser.add_argument('origin_zipcode',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )
    parser.add_argument('destiny_zipcode',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )

    def post(self) -> tuple:
        data = Courrier.parser.parse_args()
        if not Utils.validate_entry(data.pop('pakke_key')):
            return Response(message="La llave de pakke es incorrecta, verificar e intentar de nuevo").json(), 401
        courrier_services = data.pop('courrier_services')
        package = PackageModel(**data)
        package.calculate_weight()
        result = list()
        for courrier_service in courrier_services:
            if courrier_service.get('name') is None:
                result.append(Response(message={
                    "courrier_services.name": "This field cannot be blank."
                }).json())
                continue
            try:
                courrier = CourrierModel.find_courrier(courrier_service)
                if package.weight > courrier.max_weight:
                    response = Response(False,
                                        f"El peso del paquete es superior a lo permitido, peso: {package.weight}").json()
                    result.append(response)
                    continue
                price = courrier.find_prices(package)
                if courrier_service['name'] not in ["STF", 'RPK']:
                    if courrier_service['name'] == "FDX":
                        day = courrier.find_delivery_day(package)
                    else:
                        day = courrier.find_delivery_day()
                    result.append({
                        'success': True,
                        'price': price,
                        'delivery_day': day,
                        'courrier': courrier_service.get("name")
                    })
                else:
                    result.append({
                        'success': True,
                        'price': price,
                        'courrier': courrier_service.get("name")
                    })

            except CourrierErrors as e:
                res = Response(message=e.message).json()
                res['courrier'] = courrier_service.get("name")
                result.append(res)
        return {'result': result}, 200


class CourrierWieghted(Resource):
    parser = reqparse.RequestParser()
    # parser.add_argument('pakke_key',
    #                     type=str,
    #                     required=True,
    #                     help="This field cannot be blank.",
    #                     location='json'
    #                     )
    parser.add_argument('origin_zipcode',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )
    parser.add_argument('destiny_zipcode',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )

    def post(self) -> tuple:
        data = CourrierWieghted.parser.parse_args()
        data['width'] = 10
        data['height'] = 10
        data['length'] = 10
        data['weight'] = PackageModel.get_weight()
        if data['weight'] % 1 != 0:
            data['weight'] = int(data['weigth']) + 1
        result = list()
        if data['weight'] > 5:
            calc_price = 95 + ((data['weight'] - 5) * 7.5)
        else:
            calc_price = 95
        fake = {
            "success": True,
            "courrier": "Estafeta_barato",
            "delivery_day": "2018-08-10",
            "price": calc_price
        }
        result.append(fake)
        if data['weight'] > 5:
            calc_price = 249.51 + ((data['weight'] - 5) * 14.22)
        else:
            calc_price = 95
        fake = {
            "success": True,
            "courrier": "Estafeta_caro",
            "delivery_day": "2018-08-10",
            "price": calc_price
        }
        result.append(fake)
        return {'result': result,
                "weigth": data['weight']}, 200
