from flask_restful import Resource, reqparse

from app import Response
from app.common.utils import Utils
from app.models.packages.package import Package as PackageModel


class PackagePrint(Resource):
    parser = reqparse.RequestParser()
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
        try:
            PackageModel.print(**data)
            return
        except:
            return Response(message="No pudimos imprimir tu guia").json(), 400