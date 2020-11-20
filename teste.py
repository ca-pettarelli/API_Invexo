#!/usr/bin/python3
# -*- coding: UTF-8 -*-
###########################################################################
# Autor: Caroline Figueiredo Pettarelli        Project: API - Invexo      #
# Start: 26-Oct-2020       Last Update: 03-Nov-2020       Version: 1.0    #
###########################################################################

import sys
import traceback
import time
import logging
import math
import json
import requests
from datetime import datetime

LOG_FORMAT = ('%(levelname) -5s %(asctime)s %(name) -20s %(funcName) '
              '-25s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

def index():

    url = 'https://api.moskitcrm.com/v2/deals/search'
    myobj = {'field': 'CF_lXODObivipvANmaN', 'expression': 'all_of', 'values': [165206] }
    headers = {"apikey": "168ec8df-5e4f-440f-b3cd-d03b1039dff7", "Content-Type": "application/json"}
    x = requests.post(url, data = myobj, headers=headers)
    print('TESTE')
    print(x.text)
    return x.text


def main():
    index()
