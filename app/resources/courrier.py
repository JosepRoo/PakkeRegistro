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
        result = list()
        for courrier_service in courrier_services:
            if courrier_service.get('name') is None:
                result.append(Response(message={
                    "courrier_services.name": "This field cannot be blank."
                }).json())
            try:
                courrier = CourrierModel.find_courrier(courrier_service)
                price = courrier.find_prices(package)
                day = courrier.find_delivery_day(package) if courrier_service['name'] == "STF" \
                    else courrier.find_delivery_day()
                result.append({
                    'success': True,
                    'price': price,
                    'delivery_day': day,
                    'courrier': courrier.__class__.__name__
                })
            except CourrierErrors as e:
                result.append(Response(message=e.message).json())
        return {'result': result}, 200


class CourrierWieghted(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('pakke_key',
                        type=str,
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
        data['width'] = 10
        data['height'] = 10
        data['length'] = 10
        if not Utils.validate_entry(data.pop('pakke_key')):
            return Response(message="La llave de pakke es incorrecta, verificar e intentar de nuevo").json(), 401
        courrier_services = COURRIERS
        data['weight'] = PackageModel.get_weight()
        package = PackageModel(**data)
        result = list()
        for courrier_service in courrier_services:
            try:
                courrier = CourrierModel.find_courrier({'name': courrier_service})
                price = courrier.find_prices(package)
                day = courrier.find_delivery_day(package) if courrier_service['name'] == "STF" \
                    else courrier.find_delivery_day()
                result.append({
                    'success': True,
                    'price': price,
                    'delivery_day': day,
                    'courrier': courrier.__class__.__name__
                })
            except CourrierErrors as e:
                result.append(Response(message=e.message).json())
        result = sorted(result, key=itemgetter('price'))
        return {'result': result}, 200
