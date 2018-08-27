import uuid

from app.common.database import Database


class BaseModel:
    def __init__(self, _id: str = None):
        self._id = uuid.uuid4().hex if _id is None else _id

    def json(self, exclude: list = None, date_to_string: bool = True) -> dict:
        result = dict()
        for attrib in self.__dict__.keys():
            if exclude is not None and attrib in exclude:
                continue
            if type(self.__getattribute__(attrib)) is list:
                result[attrib] = list()
                for element in self.__getattribute__(attrib):
                    if not isinstance(element, str) and not isinstance(element, int):
                        result[attrib].append(element.json(date_to_string=date_to_string))
                    else:
                        result[attrib].append(element)
            else:
                result[attrib] = self.__getattribute__(attrib)
        return result

    def delete_from_mongo(self, collection: str):
        Database.remove(collection, {"_id": self._id})

    def update_mongo(self, collection: str, exclude=None):
        Database.update(collection, {"_id": self._id}, self.json(exclude, date_to_string=False))

    def save_to_mongo(self, collection: str, exclude=None):
        Database.insert(collection, self.json(exclude, date_to_string=False))

    @classmethod
    def get_by_id(cls, _id: str, collection: str):
        """
        Returns the user object with the given id, or raises an exception if that user was not found
        :param _id: id of the user to find
        :param collection: DB that contains all the users
        :return: user object
        """
        user = Database.find_one(collection, {'_id': _id})
        if user:
            return cls(**user)
