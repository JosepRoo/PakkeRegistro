from app.models.baseModel import BaseModel


class Package(BaseModel):
    def __init__(self, origin_zipcode: str, destiny_zipcode: str, weight: float, height: float, width: float,
                 length: float, _id: str = None):
        super().__init__(_id)
        self.origin_zipcode = origin_zipcode
        self.destiny_zipcode = destiny_zipcode
        self.weight = weight
        self.height = height
        self.width = width
        self.length = length
