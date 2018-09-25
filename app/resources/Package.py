from flask_restful import Resource, reqparse

from app import Response
from app.common.utils import Utils
from app.models.packages.package import Package as PackageModel


class PackagePrint(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('pakke_key',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )
    parser.add_argument('public_price',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )
    parser.add_argument('pakke_price',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )
    parser.add_argument('weight',
                        type=str,
                        required=True,
                        help="This field cannot be blank.",
                        location='json'
                        )

    def post(self):
        data = PackagePrint.parser.parse_args()
        if not Utils.validate_entry(data.pop('pakke_key')):
            return Response(message="La llave de pakke es incorrecta, verificar e intentar de nuevo").json(), 401
        try:
            PackageModel.print(**data)
            return
        except:
            return Response(message="No pudimos imprimir tu guia").json(), 400