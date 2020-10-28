#!/usr/bin/python
"""
This module is used for return variables that are in a parameters file
"""

import IniFile

PARAMETERS = IniFile.IniFileClass("config.cfg")

print PARAMETERS.find_parameter("Second", "DEF")
