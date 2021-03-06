import os
from passlib.hash import pbkdf2_sha512
import re
from functools import wraps


# utility class used thorughout other classes to perform common functions that dont fit in any other class
from app import Response
from app.models.courriers.fedex.constants import CONFIG_OBJ


class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent matches that of the database.
        The database password is encrypted more than the user's password at this stage.
        :param password: sha512-hashed password
        :param hashed_password: pbkdf2_sha512 encrypted password
        :return: True if passwords match, False otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)

    @classmethod
    def validate_entry(cls, password):
        return cls.check_hashed_password(password, os.environ.get("PAKKE_KEY"))

    @staticmethod
    def validate_keys(f):
        @wraps(f)
        def wrap(*args, **kwargs):
            if CONFIG_OBJ.account_number:
                return f(*args, **kwargs)
            else:
                return Response(message="No credentials provided.").json(), 401
        return wrap
