from app.models.baseerror import BaseError


class CourrierErrors(BaseError):
    pass


class CourrierNotFound(CourrierErrors):
    pass


class ZipCodesNotFound(CourrierErrors):
    pass


class CourrierServiceTypeUnkown(CourrierErrors):
    pass
