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

def GetInfo():
    end = int(10114 / 2)
    start = 0
    Response = {}
    for i in range(end):
        parameters = {
            "start": start,
            "limit": 2,
            "order": 'DESC',
        }
        headers = {"apikey": "a4ca266a-ef70-462f-a5bd-abc6340928b0"}

        url = "https://api.moskitcrm.com/v1/deals/"

        response = requests.get(url=url, params=parameters, headers=headers)
        response = response.json()

        if (i == 0):
            end = math.ceil(response['metadata']['pagination']['total'] / 2)

        start = start + 2

        for item in range(len(response)):
            try:
                Response['Id'] = response['results'][item]['id']
                Response['Nome'] = response['results'][item]['name']

                for ix in range(len(response['results'][item]['customFieldValues'])):
                    if (response['results'][item]['customFieldValues'][ix]['customField']['name'] == 'Bairro'):
                        Response['Bairro'] = response['results'][item]['customFieldValues'][ix]['label']

                    if (response['results'][item]['customFieldValues'][ix]['customField']['name'] == 'Empreendimento'):
                        Response['Empreendimento'] = response['results'][item]['customFieldValues'][ix]['label']

                    if (response['results'][item]['customFieldValues'][ix]['customField']['name'] == 'Origem'):
                        Response['Origem'] = response['results'][item]['customFieldValues'][ix]['value']

                    if (response['results'][item]['customFieldValues'][ix]['customField']['name'] == 'Mensagem'):
                        Response['Mensagem'] = response['results'][item]['customFieldValues'][ix]['value']

                    if (response['results'][item]['customFieldValues'][ix]['customField']['name'] == 'Qualificação Financeira'):
                        Response['Qualificação'] = response['results'][item]['customFieldValues'][ix]['label']

                Response['Data'] = str(datetime.fromtimestamp(response['results'][item]['dateCreated'] / 1000))
                LOGGER.info(Response)
                return Response

            except:
                LOGGER.info('Error')
                LOGGER.info(response)
            
        time.sleep(2.5)
    
    


def main():
    global LOGGER

    inc = sGetInfo()
    print(inc)

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