import os, requests
from datetime import datetime as dt, timedelta
from app.models.courriers.courrier import Courrier
from app.models.courriers.errors import CourrierErrors
from app.models.packages.package import Package


class UPS(Courrier):
    max_weight = 150
    username = os.environ.get('UPS_ID')
    pw = os.environ.get('UPS_PASSWORD')
    client_number = os.environ.get('UPS_CLIENT_NUMBER')
    developer_number = os.environ.get('UPS_DEVELOPER_NUMBER')
    url = os.environ.get('UPS_URL')

    def find_prices(self, package: Package) -> dict:
        json_object = {
            "UPSSecurity": {
                "UsernameToken": {
                    "Username": self.username,
                    "Password": self.pw
                },
                "ServiceAccessToken": {
                    "AccessLicenseNumber": self.developer_number
                }
            },
            "RateRequest": {
                "Request": {
                    "RequestOption": "Rate",
                    "TransactionReference": {
                        "CustomerContext": "Test Transaction"
                    }
                },
                "Shipment": {
                    "Shipper": {
                        "Name": "Promologistics",
                        "ShipperNumber": self.client_number,
                        "Address": {
                            "AddressLine": [
                                "Av. Constituyentes 908 Col. Lomas Altas"
                            ],
                            "City": "Cd. de México",
                            "StateProvinceCode": "CDMX",
                            "PostalCode": "11950",
                            "CountryCode": "MX"
                        }
                    },
                    "ShipTo": {
                        "Name": "Promologistics Client Recipient",
                        "Address": {
                            "AddressLine": [
                                ""
                            ],
                            "City": "",
                            "StateProvinceCode": "CDMX",
                            "PostalCode": package.destiny_zipcode,
                            "CountryCode": "MX"
                        }
                    },
                    "ShipFrom": {
                        "Name": "Jose Castilla",
                        "Address": {
                            "AddressLine": [
                                ""
                            ],
                            "City": "",
                            "StateProvinceCode": "CDMX",
                            "PostalCode": package.origin_zipcode,
                            "CountryCode": "MX"
                        }
                    },
                    "Service": {
                        "Code": "65",
                        "Description": "Saver"
                    },
                    "Package": {
                        "PackagingType": {
                            "Code": "02",
                            "Description": "Rate"
                        },
                        "Dimensions": {
                            "UnitOfMeasurement": {
                                "Code": "CM",
                                "Description": "centimeters"
                            },
                            "Length": str(round(package.length)),
                            "Width": str(round(package.width)),
                            "Height": str(round(package.height))
                        },
                        "PackageWeight": {
                            "UnitOfMeasurement": {
                                "Code": "KGS",
                                "Description": "kilograms"
                            },
                            "Weight": str(round(package.weight))
                        }
                    }
                }
            }
        }
        headers = {
            "Content-Type": "application/json",
            "Access-Control-Request-Headers": "Origin, X-Requested-With, Content-Type, Accept",
            "Access-Control-Request-Methods": "POST",
            "Access-Control-Allow-Origin": "*"
        }
        result = requests.post(self.url, headers=headers, json=json_object).json()
        if result.get("Fault"):
            try:
                error = result["Fault"]["detail"]["Errors"]["ErrorDetail"]["PrimaryErrorCode"]
                raise CourrierErrors("UPS answered with errors: " + error["Code"] + "-> " + error["Description"])
            except Exception as e:
                raise CourrierErrors("UPS answered with errors: " + str(e))
        amount_fields = result['RateResponse']["RatedShipment"]
        service = {'EXPRESSS_SAVER': {"price": amount_fields['TotalCharges']['MonetaryValue'],
                                      "options": {"transportation_charges": amount_fields["TransportationCharges"],
                                                  "service_options_charges": amount_fields["ServiceOptionsCharges"]}}}
        return service

    def find_delivery_day(self) -> str:
        today = dt.now()
        weekday = today.weekday()
        days = 2 if weekday == 5 else 1
        delivery_day = today + timedelta(days=days)
        return delivery_day.strftime("%Y-%m-%d")
