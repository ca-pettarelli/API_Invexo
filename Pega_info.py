#!/usr/bin/python3
# -*- coding: UTF-8 -*-
###############################################################################
# Module:   vivo-Webvendas.py              Autor: M2 Digital - Automation            #
# Start:    27-Abril-2020             Last Update: 27-Abril-2020  Version: 1.0    #
###############################################################################
#
# /usr/bin/gunicorn3 -c WebVendas-Gunicorn.cfg vivoWebVendasReservas:vivoWebVendasReservasApp

import os
import sys
import traceback
import time
import logging
import json
import multiprocessing
import mysql.connector
import requests
from datetime import datetime
from flask import Flask, request
from selenium.common.exceptions import *

LocalPath = os.path.abspath('/home/caroline/Documentos/API_Invexo') + '/'
sys.path.insert(0, LocalPath + 'inifile_python')
sys.path.insert(0, LocalPath + 'selenium-class')
sys.path.insert(0, LocalPath + 'mysql-class')

import IniFile
import SeleniumClass
import MySQLClass

LOG_FORMAT = ('%(levelname) -5s %(asctime)s %(name) -20s %(funcName) '
              '-25s %(lineno) -5d: %(message)s')
LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

# ConfigFileName = LocalPath + 'init.cfg'
# PARAMETERS = IniFile.IniFileClass(ConfigFileName)

# DbObj = MySQLClass.MySQLClass(PARAMETERS.find_parameter("MySQL", "User"),
#                               PARAMETERS.find_parameter("MySQL", "Pass"),
#                               PARAMETERS.find_parameter("MySQL", "Db"),
#                               PARAMETERS.find_parameter("MySQL", "Host"),
#                               int(PARAMETERS.find_parameter("MySQL", "Port")),
#                               False, True)

vivoWebVendasReservasApp = Flask(__name__)
vivoWebVendasReservasPath = "/"
vivoWebVendasReservasPort = 5002

Selenium = ''
APITime = 0
RequestId = 0
RequestStr = ""
APITimeStr = ""


def Wait(v_Selenium, v_TimeOut=None, v_ContextReturn=None):
    global LOGGER

    WaitTimeOut = 1
    TimeOut = v_TimeOut
    if (v_TimeOut is None):
        TimeOut = (v_Selenium.StepTimeout * 2)

    LOGGER.info('Wait Start (' + str(TimeOut) + ')')

    if (v_ContextReturn is not None):
        v_Selenium.SwitchContext("DEFAULT")

    ElmClass = "lojaProgressDialog"
    for Idx in range(TimeOut):
        time.sleep(WaitTimeOut)
        if (len(v_Selenium.Browser.find_elements_by_class_name(ElmClass)) == 0):
            break

        for WaitObj in v_Selenium.Browser.find_elements_by_class_name(ElmClass):
            WaitObjStyle = str(WaitObj.get_attribute("style"))
            LOGGER.info("WaitObjStyle: '" + WaitObjStyle + "'")

    if (v_ContextReturn is not None):
        v_Selenium.SwitchContext(v_ContextReturn)

    LOGGER.info('Wait End')


def ClientPage(v_Selenium, page):
    global LOGGER

    try:
        v_Selenium.Browser.get(page)
        time.sleep(2)

        LOGGER.info('ClientPage - Loaded Successfully')

        list_of_ps = []

        content_blocks = Selenium.Browser.find_elements_by_class_name("row")
        # print('Content blocks: ' + str(content_blocks))

        for block in content_blocks:
            try:
                elements = block.find_elements_by_tag_name('p')
                for el in elements:
                    list_of_ps.append(el.text)
                # print('Elements: ' + str(elements))
                # print('Text: ' + str(elements.text))
            except:
                pass

        # print(list_of_ps)

    except Exception as Exc:
        LOGGER.info('ClientPage Exception (' + str(Exc).strip() + ')')
    
    return list_of_ps


def LoginIntoSystem(v_Selenium):
    global LOGGER

    v_Selenium.Browser.get('https://developers.moskitcrm.com/docs/api-v1/spec-api-v1.yaml/paths/~1deals/get')
    LOGGER.info('Browser Oppened')
    Wait(v_Selenium)


def makeFile(infos, Aindex):
    # print(infos)
    Aindex = '#00' + str(Aindex)

    arquivo = open('arq' + Aindex + '.vcf','w')
    for client in infos:
        arquivo.write("BEGIN:VCARD\n")
        arquivo.write("VERSION:2.1\n")
        index = 0
        for inf in client:
            if ('Razão Social' in inf):
                name = index
            if ('Telefone' in inf):
                tel = index
            index = index + 1
        Clientname = client[name].replace('Razão Social:', '')
        Clientname = str(Aindex) + ' ' + str(Clientname)
        arquivo.write("N:;" + Clientname.strip() + ";;;\n")
        arquivo.write("FN:" + Clientname.strip() + "\n")
        if ('Telefone(s):\n' in client[tel]):
            tel = client[tel].replace('Telefone(s):\n', '')
        if('(Ligar)' in tel):
            tel = tel.replace('(Ligar)', '')
        if('(Whatsapp)' in tel):
            tel = tel.replace('(Whatsapp)', '')
        if ('(' in tel):
            tel = tel.replace('(', '')
        if (')' in tel):
            tel = tel.replace(')', '')
        if ('-' in tel):
            tel = tel.replace('-', '')
        if (' ' in tel):
            tel = tel.replace(' ', '')
           
        arquivo.write("TEL;CELL;PREF:" + tel.strip() + "\n")
        arquivo.write("END:VCARD\n")
    arquivo.close()


def AppOrchestrator(texto):
    global LOGGER, Selenium

    sReturn = ''
    OrchestratorTime = datetime.utcnow().timestamp()
    v_Selenium.ClickButton("bp3-tab-title_RequestMaker__RequestEditor-tabs_request-headers", "id")

    # Content = True
    # index = 1
    # while (Content):
    #     list_of_hrefs = []
    #     content_blocks = Selenium.Browser.find_elements_by_class_name("hero")

    #     for block in content_blocks:
    #         elements = block.find_elements_by_tag_name("a")
    #         for el in elements:
    #             list_all = el.get_attribute("href")
    #             if (list_all not in list_of_hrefs):
    #                 list_of_hrefs.append(list_all)

    #     print(list_of_hrefs)
    #     del(list_of_hrefs[0])

    #     if ('empresa' in list_of_hrefs[-1]):
    #         nextPage = list_of_hrefs[-1]
    #         del(list_of_hrefs[-1])
    #         ultima = False
    #     else:
    #         ultima = True
        
    #     infos = []
    #     for link in list_of_hrefs:
    #         infos.append(ClientPage(Selenium, link))
        
    #     makeFile(infos, index)

    #     if (ultima is False):
    #         Selenium.Browser.get(nextPage)
    #         LOGGER.info('Browser Oppened')
    #         Wait(Selenium)
    #         Content = True
    #         index = index + 1
    #     else:
    #         Content = False

    # OrchestratorTime = ((datetime.utcnow().timestamp() - OrchestratorTime) *
    #                     1000)
    # LOGGER.info('Orchestrator Total Time %.3f ms' % (OrchestratorTime))

    # if (len(sReturn) == 0):
    #     sReturn = Response(-1, 'System Exception')

    
    return sReturn


def Response(v_MsgCode, v_Payload, v_Message=''):
    global LOGGER, APITime

    RespArr = [-1, "-1", "Abnormal Program Error", "Abnormal Program Error"]
    # jReturn= {}

    # if ((v_Message is None) or (v_Message == '')):
    #     v_Message = v_Payload

    if (v_MsgCode == 100):
        RespArr = [0, str(v_MsgCode), v_Payload, v_Message]
    else:
        RespArr = [-1, str(v_MsgCode), v_Payload, v_Message]

    APITime = ((datetime.utcnow().timestamp() - APITime) * 1000)
    APIRequestTimeStr = '%.3f' % (APITime)

    # jReturn = json.dumps({'Status': RespArr[0],
    #                       'MsgCode': int(RespArr[1]),
    #                       'ApiTimeMS': float(APIRequestTimeStr),
    #                       'Payload': RespArr[2],
    #                       'Message': RespArr[3]}, ensure_ascii=False)

    jReturn = {'Status': RespArr[0],
                          'MsgCode': int(RespArr[1]),
                          'ApiTimeMS': float(APIRequestTimeStr),
                          'Payload': RespArr[2],
                          'Message': RespArr[3]
    }


    # jReturn['Status'] = RespArr[0]
    # jReturn['MsgCode'] = int(RespArr[1])
    # jReturn['ApiTimeMS'] = float(APIRequestTimeStr)
    # jReturn['Payload'] = RespArr[2]
    # jReturn['Message'] = RespArr[3]
    
    # jReturn = json.dumps({jReturn}, ensure_ascii=False)
    print('4' + str(type(jReturn)))
    return jReturn


def SaveToDb(v_VivoData, v_Client):
    global LOGGER, DbObj

    jData = json.loads(v_VivoData)
    jPayload = jData['Payload']
    LOGGER.info(jData)
    SqlArr = []
    for Item in jPayload:
        ItemListId = 0

        ItemStr = str(jPayload[Item])
        ItemCode = str(jData['MsgCode'])
        if (ItemStr[:3] == "ERR"):
            ItemCode = "-1"

        if (type(jPayload[Item]) == list):
            for ItemList in jPayload[Item]:
                ItemListId = ItemListId + 1
                ItemStr = str(ItemList)

                sSql = ("INSERT INTO m2vivo.m2_retorno_360 (dt_consulta, " +
                        "status, cpf_cliente, id_produto, nome_produto) " +
                        "VALUES (NOW(), '" + ItemCode + "', '" +
                        str(v_Client.CPF) + "', " + str(ItemListId) + ", " +
                        "'" + ItemStr + "')")
                SqlArr.append(sSql)
        else:
            sSql = ("INSERT INTO m2vivo.m2_retorno_360 (dt_consulta, " +
                    "status, cpf_cliente, id_produto, nome_produto) " +
                    "VALUES (NOW(), '" + ItemCode + "', '" +
                    str(v_Client.CPF) + "', " + str(ItemListId) + ", " +
                    "'" + ItemStr + "')")
            SqlArr.append(sSql)
    try:
        for sSql in SqlArr:
            LOGGER.info(sSql)
            # DbObj.Execute(sSql)
            # DbObj.Commit()
    except Exception as Exc:
        LOGGER.info('Db Exception (' + str(Exc).strip() + ')')
        LOGGER.info(jPayload)
        LOGGER.info(sSql)


def ProcessBatch():

    global LOGGER, LocalPath, Selenium

    # GlobalTimeout = int(PARAMETERS.find_parameter("General", "GlobalTimeout"))

    # AllObjReturn = GetProcessBatch()
    # LOGGER.info('Total de CPFs serem processados: ' + str(len(AllObjReturn)))
    texto = 'ola'
    # time.sleep(1000)
    AppOrchestrator(texto)
    # try:
    #     LOGGER.info('========== Starting Process (Timeout: ' +
    #                 str(GlobalTimeout) + ') ==========')
    #     pPool = multiprocessing.Pool(processes=1)
    #     pProc = pPool.apply_async(AppOrchestrator,
    #                                 args=( texto, ))
    #     sReturn = pProc.get(GlobalTimeout)
    #     # SaveToDb(sReturn, Client)
    #     LOGGER.info('========== Ending Process ==========')
    # except multiprocessing.context.TimeoutError:
    #     # SaveToDb(Response(-1, {'ID_00': 'TimeOut'}), Client)
    #     LOGGER.info('TimeOut (' + str(GlobalTimeout) + ' s)')
    # except Exception as Exc:
    #     # SaveToDb(Response(-1, {'ERROR': 'MaxRetires / Others'}), Client)
    #     LOGGER.info('ERROR: MaxRetires / Others (' +
    #                 str(Exc).strip() + '): ' +
    #                 str(sys.exc_info()).strip())
    # finally:
    #     pPool.close()


def main():
    global vivoWebVendasReservasApp
    global LOGGER, LocalPath, APITime, Selenium

    Selenium = SeleniumClass.SeleniumClass(True, LocalPath)
    Selenium.Browser.set_window_size(1920, 720)
    LoginIntoSystem(Selenium)
    # time.sleep(600)
    # vivoWebVendasReservasApp.run(host="0.0.0.0")
    ProcessBatch()
    Selenium.Quit()


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