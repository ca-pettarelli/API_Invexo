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
    end = 100000
    start = 0
    Response = {}
    for i in range(end):
    myobj = [
        {
        "field": "CF_lXODObivipvANmaN",
        "expression": "all_of",
        "values": [
            165206
        ]
        }
    ]

    parameters = {
            "start": start,
            "limit": 2,
            "order": 'DESC',
            'quantity': end,
        }

    headers = {"apikey": "168ec8df-5e4f-440f-b3cd-d03b1039dff7", "Content-Type": "application/json"}

    response = requests.post('https://api.moskitcrm.com/v2/deals/search', params=parameters, json=myobj, headers=headers)

    print("Status code: ", response.status_code)

    response_Json = response.json()
    print("Printing Entire Post Request")
    # print(response_Json)
    
    print("Content-Type is ", response.headers['X-Moskit-Listing-Quantity'])
    return response.json()


def main():
    global LOGGER

    teste = index()
    print(teste)

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as Exc:
        LOGGER.info('General Error (' + str(Exc) + ') - ' +
                    str(sys.exc_info()))
        traceback.print_exc(file=sys.stdout)
        sys.exit(1)
    except KeyboardInterrupt:
        print("Process Interrupted!")
        sys.exit(1)
