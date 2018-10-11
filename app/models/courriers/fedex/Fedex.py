from fedex.services.rate_service import FedexRateServiceRequest

from app.common.utils import Utils
from app.models.courriers.courrier import Courrier
from app.models.courriers.estafeta.estafeta import Estafeta
from app.models.courriers.fedex.constants import CONFIG_OBJ
from app.models.packages.package import Package


class Fedex(Courrier):
    @Utils.validate_keys
    def find_prices(self, package: Package) -> dict:
        """
        given a list or str of courrier types it will get the prices for each one
        :param package: Package detail
        :return: dict for each service to calculate with the price as value
        """
        service_prices = dict()

        # This is the object that will be handling our request.
        rate = FedexRateServiceRequest(CONFIG_OBJ)

        # This is very generalized, top-level information.
        # REGULAR_PICKUP, REQUEST_COURIER, DROP_BOX, BUSINESS_SERVICE_CENTER or STATION
        rate.RequestedShipment.DropoffType = 'REGULAR_PICKUP'

        # See page 355 in WS_ShipService.pdf for a full list. Here are the common ones:
        # STANDARD_OVERNIGHT, PRIORITY_OVERNIGHT, FEDEX_GROUND, FEDEX_EXPRESS_SAVER
        # To receive rates for multiple ServiceTypes set to None.
        rate.RequestedShipment.ServiceType = None

        # What kind of package this will be shipped in.
        # FEDEX_BOX, FEDEX_PAK, FEDEX_TUBE, YOUR_PACKAGING
        rate.RequestedShipment.PackagingType = 'YOUR_PACKAGING'

        # Shipper's address
        rate.RequestedShipment.Shipper.Address.PostalCode = package.origin_zipcode
        rate.RequestedShipment.Shipper.Address.CountryCode = 'MX'

        # Recipient address
        rate.RequestedShipment.Recipient.Address.PostalCode = package.destiny_zipcode
        rate.RequestedShipment.Recipient.Address.CountryCode = 'MX'

        # This is needed to ensure an accurate rate quote with the response.
        # rate_request.RequestedShipment.Recipient.Address.Residential = True
        # include estimated duties and taxes in rate quote, can be ALL or NONE
        rate.RequestedShipment.EdtRequestType = 'NONE'

        # Who pays for the rate_request?
        # RECIPIENT, SENDER or THIRD_PARTY
        rate.RequestedShipment.ShippingChargesPayment.PaymentType = 'SENDER'

        # WSDL to manage the weight property
        package1_weight = rate.create_wsdl_object_of_type('Weight')
        # Weight, in KG.
        package1_weight.Value = package.weight
        package1_weight.Units = "KG"

        # WSDL to manage the dimensions properties
        # Optional but recommended if your package type is YOUR_PACKAGING.
        package1_dimensions = rate.create_wsdl_object_of_type('Dimensions')
        # Height, Width, and Length, in CM.
        package1_dimensions.Height = int(package.height)
        package1_dimensions.Width = int(package.width)
        package1_dimensions.Length = int(package.length)
        package1_dimensions.Units = "CM"

        package1 = rate.create_wsdl_object_of_type('RequestedPackageLineItem')
        package1.Weight = package1_weight
        package1.Dimensions = package1_dimensions

        # can be other values this is probably the most common
        package1.PhysicalPackaging = 'BOX'

        # Required, but according to FedEx docs:
        # "Used only with PACKAGE_GROUPS, as a count of packages within a
        # group of identical packages". In practice you can use this to get rates
        # for a shipment with multiple packages of an identical package size/weight
        # on rate request without creating multiple RequestedPackageLineItem elements.
        # You can OPTIONALLY specify a package group:
        # package1.GroupNumber = 0  # default is 0
        # The result will be found in RatedPackageDetail, with specified GroupNumber.
        package1.GroupPackageCount = 1

        # This adds the RequestedPackageLineItem WSDL object to the rate_request. It
        # increments the package count and total weight of the rate_request for you.
        rate.add_package(package1)

        # Fires off the request, sets the 'response' attribute on the object.
        rate.send_request()

        # This will convert the response to a python dict object. To
        # make it easier to work with.
        # from fedex.tools.conversion import basic_sobject_to_dict
        # print(basic_sobject_to_dict(rate.response))

        # This will dump the response data dict to json.
        # from fedex.tools.conversion import sobject_to_json
        # result = sobject_to_json(rate.response)
        # print(result)

        # RateReplyDetails can contain rates for multiple ServiceTypes if ServiceType was set to None
        for service in rate.response.RateReplyDetails:
            for detail in service.RatedShipmentDetails:
                for surcharge in detail.ShipmentRateDetail.Surcharges:
                    if surcharge.SurchargeType == 'OUT_OF_DELIVERY_AREA':
                        pass
                        # print("{}: ODA rate_request charge {}".format(service.ServiceType, surcharge.Amount.Amount))

            for rate_detail in service.RatedShipmentDetails:
                service_prices[service.ServiceType] =\
                    rate_detail.ShipmentRateDetail.TotalNetChargeWithDutiesAndTaxes.Amount
                # print("{}: Net FedEx Charge {} {}".format(service.ServiceType,
                #                                           rate_detail.ShipmentRateDetail.TotalNetFedExCharge.Currency,
                #                                           rate_detail.ShipmentRateDetail.TotalNetChargeWithDutiesAndTaxes.Amount))

        return service_prices

    def find_delivery_day(self, package: Package) -> str:
        """
        given the courrier, depending on each one it will calculate the day estimated of completed delivery
        :return: str with datetime data
        """
        estafeta = Estafeta(self)
        return estafeta.find_delivery_day(package)

    def set_type(self) -> None:
        """sets the type of the courrier if it wasn't set at __init__"""
        pass
