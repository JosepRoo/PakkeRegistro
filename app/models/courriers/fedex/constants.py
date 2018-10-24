import os
from fedex.config import FedexConfig

WS_URL = os.environ.get('FEDEX_URL')

"""
This file holds various configuration options used for Fedex services
"""

CONFIG_OBJ = FedexConfig(key=os.environ.get('FEDEX_KEY'),
                         password=os.environ.get('FEDEX_PW'),
                         account_number=os.environ.get('FEDEX_ACC_NO'),
                         meter_number=os.environ.get('FEDEX_METER_NO'),
                         use_test_server=False)
