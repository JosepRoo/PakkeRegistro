from app import Courrier
from app.models.packages.package import Package


class Fedex(Courrier):
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
