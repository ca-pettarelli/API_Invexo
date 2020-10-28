#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import os
import logging
import pickle
import requests
import json
import time
import re
from datetime import date, timedelta, datetime

from selenium.webdriver import Ie as IeWebBrowser
from selenium.webdriver.ie.options import Options as IeOptions
from selenium.webdriver import Chrome as ChWebBrowser
from selenium.webdriver.chrome.options import Options as ChOptions
from selenium.webdriver import Firefox as GkWebBrowser
from selenium.webdriver.firefox.options import Options as GkOptions

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import *

LOGGER = logging.getLogger(__name__)


# General Class
class SeleniumClass(object):
    def __init__(self, v_bShow=False, v_WorkingPath='', v_UseCookies=False,
                 v_Engine='Chrome',
                 v_EngineDriver=None):
        LOG_FORMAT = ('%(levelname) -5s %(asctime)s %(name) -20s %(funcName) '
                      '-25s %(lineno) -5d: %(message)s')

        logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)

        self.StepTimeout = 15
        self.WaitTimeout = 2
        self.CookiesFile = ''
        self.UseCookies = v_UseCookies
        self.Engine = v_Engine
        self.EngineDriver = v_EngineDriver
        self.EngineDriverPath = ''

        if (v_WorkingPath != ''):
            LOGGER.info('WorkingPath: ' + os.path.realpath(v_WorkingPath))
            if (self.Engine == 'IE'):
                self.CookiesFile = os.path.realpath(v_WorkingPath) + '\\cookies.pkl'
            else:
                self.CookiesFile = os.path.realpath(v_WorkingPath) + '/cookies.pkl'

        if (self.Engine == 'Chrome'):
            self.EngineDriver = '/usr/local/sbin/chromedriver'
            opts = ChOptions()
            opts.add_argument("binary_location = '/usr/bin/'")
        elif (self.Engine == 'IE'):
            opts = IeOptions()
            opts.add_argument("binary_location = 'C:\\Program Files (x86)\\Internet Explorer'")
        elif (self.Engine == 'Firefox'):
            self.EngineDriver = '/usr/local/sbin/geckodriver'
            self.EngineDriver = '/usr/local/sbin'
            opts = GkOptions()
            opts.add_argument("binary_location = '/usr/bin/'")

        LOGGER.info('Engine: ' + self.Engine)
        LOGGER.info('EngineDriver: ' + self.EngineDriver)

        self.EngineDriverPath = os.path.dirname(os.path.abspath(self.EngineDriver))
        sys.path.insert(0, self.EngineDriverPath)

        opts.add_argument("--start-maximized")
        opts.add_argument("--enable-automation")
        opts.add_argument("--log-level=3")
        opts.add_argument("--silent")
        opts.add_argument("--disable-infobars")
        opts.add_argument("--disable-dev-shm-usage")
        opts.add_argument("--disable-browser-side-navigation")
        opts.add_argument("--disable-gpu")
        opts.add_argument("--no-sandbox")
        opts.add_argument("--no-zygote")
        if (not v_bShow):
            LOGGER.info('Headless Operation')
            opts.add_argument("--headless")
            opts.add_argument("--disable-setuid-sandbox")

        if (self.Engine == 'Chrome'):
            self.Browser = ChWebBrowser(self.EngineDriver, options=opts)
        elif (self.Engine == 'IE'):
            self.Browser = IeWebBrowser(self.EngineDriver, options=opts)
        elif (self.Engine == 'Firefox'):
            self.Browser = GkWebBrowser(self.EngineDriver, options=opts)

        if (self.UseCookies):
            try:
                if ((self.CookiesFile != '') and (os.path.isfile(self.CookiesFile))):
                    for cookie in pickle.load(open(self.CookiesFile, "rb")):
                        self.Browser.add_cookie(cookie)
                    LOGGER.info('Cookies Loaded')
            except Exception as Exc:
                LOGGER.info('Could Not Load Cookies ' + self.CookiesFile +
                            ' - (' + str(Exc).strip() + ')')

        self.Browser.set_window_size(1920, 1080)
        self.Browser.set_window_position(0, 0)

    def SwitchContext(self, v_ObjIdentity, v_TypeOfIdentity='ID', v_TimeOut=None):
        if (v_TimeOut is None):
            v_TimeOut = self.StepTimeout

        v_TimeOut = 0.5

        LOGGER.info("ObjIdentity: " + str(v_ObjIdentity) +
                    " (" + str(v_TypeOfIdentity).strip().upper() + ")" +
                    "; TimeOut: " + str(v_TimeOut))

        CtxReturn = False

        try:
            if (type(v_ObjIdentity) == int):
                self.Browser.switch_to.frame(v_ObjIdentity)
                CtxReturn = True
            else:
                if ((str(v_ObjIdentity).strip().upper() == 'DEFAULT') or
                   (str(v_ObjIdentity).strip().upper() == 'MAIN')):
                    self.Browser.switch_to.default_content()
                    CtxReturn = True
                else:
                    frmElm = self.GetElement(v_ObjIdentity, v_TypeOfIdentity,
                                             v_TimeOut)
                    if (frmElm is False):
                        LOGGER.info('iFrame "' + v_ObjIdentity + '" not founded')
                        CtxReturn = False
                        raise TimeoutException
                    else:
                        self.Browser.switch_to.frame(frmElm)
                        CtxReturn = True
        except Exception as Exc:
            LOGGER.info('Could Switch to iFrame (' + str(Exc).strip() + ')')
            CtxReturn = False

        return CtxReturn

    def FindElement(self, v_ObjIdentity, v_TypeOfIdentity='ID', v_TimeOut=None):
        if (v_TimeOut is None):
            v_TimeOut = self.StepTimeout

        bReturn = False

        LOGGER.info("ObjIdentity: " + v_ObjIdentity +
                    " (" + v_TypeOfIdentity.strip().upper() + ")" +
                    "; TimeOut: " + str(v_TimeOut))

        wait = WebDriverWait(self.Browser, v_TimeOut)

        if (v_TypeOfIdentity.strip().upper() == 'JSID'):
            try:
                for IdTime in range(v_TimeOut - 1):
                    JsCode = ("document.getElementById('" +
                              v_ObjIdentity + "');")
                    JsReturn = self.ExecJsScript(JsCode, True)
                    if 'webdriver.remote.webelement.WebElement' in JsReturn:
                        break
                    time.sleep(1)
            except NoSuchElementException:
                bReturn = False
            except TimeoutException:
                bReturn = False
            bReturn = True
        elif (v_TypeOfIdentity.strip().upper() == 'JSXPATH'):
            try:
                for IdTime in range(v_TimeOut - 1):
                    JsCode = ("document.evaluate(" + v_ObjIdentity + ", " +
                              "document, null, " +
                              "XPathResult.FIRST_ORDERED_NODE_TYPE, null" +
                              ");")
                    JsReturn = self.ExecJsScript(JsCode, True)
                    if 'webdriver.remote.webelement.WebElement' in JsReturn:
                        break
                    time.sleep(1)
            except NoSuchElementException:
                bReturn = False
            except TimeoutException:
                bReturn = False
            bReturn = True
        elif (v_TypeOfIdentity.strip().upper() == 'JSCLASS'):
            try:
                for IdTime in range(v_TimeOut - 1):
                    JsCode = ("document.getElementsByClassName('" +
                              v_ObjIdentity + "')[0];")
                    JsReturn = self.ExecJsScript(JsCode, True)
                    if 'webdriver.remote.webelement.WebElement' in JsReturn:
                        break
                    time.sleep(1)
            except NoSuchElementException:
                bReturn = False
            except TimeoutException:
                bReturn = False
            bReturn = True
        elif (v_TypeOfIdentity.strip().upper() == 'JSNAME'):
            try:
                for IdTime in range(v_TimeOut - 1):
                    JsCode = ("document.getElementsByName('" +
                              v_ObjIdentity + "')[0];")
                    JsReturn = self.ExecJsScript(JsCode, True)
                    if 'webdriver.remote.webelement.WebElement' in JsReturn:
                        break
                    time.sleep(1)
            except NoSuchElementException:
                bReturn = False
            except TimeoutException:
                bReturn = False
            bReturn = True
        elif (v_TypeOfIdentity.strip().upper() == 'JSCSS'):
            try:
                for IdTime in range(v_TimeOut - 1):
                    JsCode = ("document.querySelectorAll('" +
                              v_ObjIdentity + "')[0];")
                    JsReturn = self.ExecJsScript(JsCode, True)
                    if 'webdriver.remote.webelement.WebElement' in JsReturn:
                        break
                    time.sleep(1)
            except NoSuchElementException:
                bReturn = False
            except TimeoutException:
                bReturn = False
            bReturn = True
        elif (v_TypeOfIdentity.strip().upper() == 'ID'):
            try:
                wait.until(expected_conditions.visibility_of_element_located(
                           (By.ID, v_ObjIdentity)))
                self.Browser.find_element_by_id(v_ObjIdentity)
            except NoSuchElementException:
                bReturn = False
            except TimeoutException:
                bReturn = False
            bReturn = True
        elif (v_TypeOfIdentity.strip().upper() == 'XPATH'):
            try:
                wait.until(expected_conditions.visibility_of_element_located(
                           (By.XPATH, v_ObjIdentity)))
                self.Browser.find_element_by_xpath(v_ObjIdentity)
            except NoSuchElementException:
                bReturn = False
            except TimeoutException:
                bReturn = False
            bReturn = True
        elif (v_TypeOfIdentity.strip().upper() == 'CLASS'):
            try:
                wait.until(expected_conditions.visibility_of_element_located(
                           (By.CLASS_NAME, v_ObjIdentity)))
                self.Browser.find_element_by_class_name(v_ObjIdentity)
            except NoSuchElementException:
                bReturn = False
            except TimeoutException:
                bReturn = False
            bReturn = True
        elif (v_TypeOfIdentity.strip().upper() == 'NAME'):
            try:
                wait.until(expected_conditions.visibility_of_element_located(
                           (By.NAME, v_ObjIdentity)))
                self.Browser.find_element_by_name(v_ObjIdentity)
            except NoSuchElementException:
                bReturn = False
            except TimeoutException:
                bReturn = False
            bReturn = True
        elif (v_TypeOfIdentity.strip().upper() == 'CSS'):
            try:
                wait.until(expected_conditions.visibility_of_element_located(
                           (By.CSS_SELECTOR, v_ObjIdentity)))
                self.Browser.find_element_by_css_selector(v_ObjIdentity)
            except NoSuchElementException:
                bReturn = False
            except TimeoutException:
                bReturn = False
            bReturn = True

        if (bReturn):
            LOGGER.info("ObjIdentity: " + v_ObjIdentity +
                        " (" + v_TypeOfIdentity.strip().upper() + "); " +
                        "FOUNDED")
        else:
            LOGGER.info("ObjIdentity: " + v_ObjIdentity +
                        " (" + v_TypeOfIdentity.strip().upper() + "); " +
                        "NOT FOUNDED")

        return bReturn

    def GetElement(self, v_ObjIdentity, v_TypeOfIdentity='ID', v_TimeOut=None):
        if (v_TimeOut is None):
            v_TimeOut = self.StepTimeout

        LOGGER.info("ObjIdentity: " + v_ObjIdentity +
                    " (" + v_TypeOfIdentity.strip().upper() + "); " +
                    "TimeOut: " + str(v_TimeOut))

        ElmReturn = False

        try:
            if (self.FindElement(v_ObjIdentity, v_TypeOfIdentity, v_TimeOut)):
                if ((v_TypeOfIdentity.strip().upper() == 'ID') or
                   (v_TypeOfIdentity.strip().upper() == 'JSID')):
                    ElmReturn = self.Browser.find_element_by_id(v_ObjIdentity)
                elif (v_TypeOfIdentity.strip().upper() == 'XPATH'):
                    ElmReturn = self.Browser.find_element_by_xpath(v_ObjIdentity)
                elif (v_TypeOfIdentity.strip().upper() == 'CLASS'):
                    ElmReturn = self.Browser.find_element_by_class_name(v_ObjIdentity)
                elif (v_TypeOfIdentity.strip().upper() == 'NAME'):
                    ElmReturn = self.Browser.find_element_by_name(v_ObjIdentity)
                elif (v_TypeOfIdentity.strip().upper() == 'CSS'):
                    ElmReturn = self.Browser.find_element_by_css_selector(v_ObjIdentity)
            else:
                ElmReturn = False
        except NoSuchElementException:
            ElmReturn = False
        except TimeoutException:
            ElmReturn = False

        if (ElmReturn):
            LOGGER.info("ObjIdentity: " + v_ObjIdentity +
                        " (" + v_TypeOfIdentity.strip().upper() + "); " +
                        "ELEMENT OK")
        else:
            LOGGER.info("ObjIdentity: " + v_ObjIdentity +
                        " (" + v_TypeOfIdentity.strip().upper() + "); " +
                        "ELEMENT NOT OK")

        return ElmReturn

    def ExecJsScript(self, v_JsScript, v_ReturnValue=True, v_Verbose=False):
        if (v_ReturnValue):
            JsScript = 'return ' + v_JsScript
        else:
            JsScript = v_JsScript

        if (v_Verbose):
            LOGGER.info("ExecJsScript: " + JsScript)

        JsReturn = str(self.Browser.execute_script(JsScript))

        if (v_ReturnValue):
            if (v_Verbose):
                LOGGER.info(JsReturn)

            return JsReturn