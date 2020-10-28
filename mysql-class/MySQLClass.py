#!/usr/bin/python3
# -*- coding: UTF-8 -*-
###############################################################################
# Module:   MySQLClass.py              Autor: Felipe Almeida                  #
# Start:    14-Nov-2019                Last Update: 14-Nov-2019  Version: 1.0 #
###############################################################################

import os
import logging
import mysql.connector
from datetime import datetime

LOGGER = logging.getLogger(__name__)


class MySQLClass(object):
    DbConn = False

    def __init__(self, v_User='', v_Pass='', v_MyDb='', v_Host='127.0.0.1',
                 v_Port=3306, v_AutoConnect=True, v_Verbose=False,
                 v_TimeOut=300):
        LOG_FORMAT = ('%(levelname) -5s %(asctime)s %(name) -25s %(funcName) '
                      '-25s %(lineno) -5d: %(message)s')

        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

        self.User = v_User
        self.Pass = v_Pass
        self.MyDb = v_MyDb
        self.Host = v_Host
        self.Port = v_Port
        self.Verbose = v_Verbose
        self.TimeOut = v_TimeOut

        if (v_AutoConnect):
            self.Connect()

    def Connect(self):
        self.DbConn = mysql.connector.connect(host=self.Host, port=self.Port,
                                              user=self.User, passwd=self.Pass,
                                              database=self.MyDb,
                                              connection_timeout=self.TimeOut)
        self.DbCursor = self.DbConn.cursor(prepared=True)
        if (self.DbConn.is_connected() and self.Verbose):
            LOGGER.info("Connected to MySQL (" +
                        self.Host + ":" +
                        str(self.Port) + " / " +
                        self.User + ")")

    def IsConnected(self):
        if (self.DbConn is False):
            return False

        if (self.DbConn.is_connected()):
            return True
        else:
            return False

    def Close(self):
        if (self.IsConnected()):
            self.DbCursor.close()
            self.DbConn.close()
            if (self.Verbose):
                LOGGER.info("Disconnected from MySQL (" + self.Host + " / " +
                      self.User + ")")

    def Commit(self):
        self.DbConn.commit()
        if (self.Verbose):
            LOGGER.info("Commited to MySQL")

    def Rows(self):
        if (self.DbConn.is_connected()):
            return self.DbCursor.rowcount
        else:
            return -1

    def Execute(self, v_Query='', v_QueryParams=None):
        if (len(v_Query) > 0):
            try:
                if (not self.DbConn.is_connected()):
                    self.Connect()

                if (v_QueryParams is None):
                    self.DbCursor.execute(v_Query)
                else:
                    self.DbCursor.execute(v_Query, v_QueryParams)
            except mysql.connector.Error as error:
                if (self.Verbose):
                    LOGGER.info("Parameterized query failed {}".format(error))
                    LOGGER.info(v_Query)
        else:
            return []

    def QueryAll(self, v_Query='', v_QueryParams=None):
        if (len(v_Query) > 0):
            self.Execute(v_Query, v_QueryParams)
            sqlReturn = self.DbCursor.fetchall()
            self.Commit()  # Clear Cache
            return sqlReturn
        else:
            return []

    def QueryOne(self, v_Query='', v_QueryParams=None):
        if (len(v_Query) > 0):
            self.Execute(v_Query, v_QueryParams)
            sqlReturn = self.DbCursor.fetchone()
            self.Commit()  # Clear Cache
            return sqlReturn
        else:
            return []

    def FixData(self, v_Data='', v_DataType='STR', v_Strip=True):
        ThisData = v_Data

        if ThisData is None:
            sReturn = "NULL"
        elif isinstance(ThisData, bool):
            if (ThisData):
                sReturn = "'TRUE'"
            else:
                sReturn = "'FALSE'"
        elif isinstance(ThisData, float):
            sReturn = ThisData
        elif isinstance(ThisData, datetime):
            if (str(ThisData) == 'NaT'):
                sReturn = "NULL"
            else:
                sReturn = "STR_TO_DATE('" + ThisData.strftime("%d/%m/%Y") + "','%d/%m/%Y')"
        elif isinstance(ThisData, str):
            if (v_Strip):
                ThisData = ThisData.strip()
            if (len(ThisData) == 0):
                sReturn = "NULL"
            else:
                if (v_DataType.strip().upper() == 'STR'):
                    sReturn = "'" + str(ThisData).replace('"', '""').replace("'", "''") + "'"
                elif (v_DataType.strip().upper() == 'NUM'):
                    try:
                        sReturn = '%.2f' % float(str(ThisData).replace(" ", ""))
                    except:
                        sReturn = '%.2f' % float(str(ThisData).replace(".", "").replace(",", ".").replace(" ", ""))
                    if ('.00' in sReturn):
                        sReturn = sReturn.replace('.00', '')
                elif (v_DataType.strip().upper() == 'DATE'):
                    sReturn = "STR_TO_DATE('" + ThisData + "','%d/%m/%Y')"
        else:
            sReturn = "'" + str(ThisData).replace('"', '""').replace("'", "''") + "'"

        if ((str(sReturn) == "'nan'") or (str(sReturn) == "nan")):
            sReturn = "NULL"

        if ((sReturn == "'n/d'") or (sReturn == "n/d")):
            sReturn = "NULL"

        if (sReturn == "'-'"):
            sReturn = "NULL"

        if ((sReturn.strip() == "") or (sReturn.strip() == "''") or
           (sReturn.strip() == "SN") or (sReturn.strip() == "'SN'")):
            sReturn = "NULL"

        return str(sReturn)