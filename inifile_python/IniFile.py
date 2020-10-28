#!/usr/bin/python3
# -*- coding: UTF-8 -*-
"""
This class is used for return variables that are in a parameters file
"""


class IniFileClass(object):
    """
    This class is used for return variables that are in a parameters file
    """

    def __init__(self, v_FileName, v_Verbose=False):
        """
        Object initialization
        """
        self.FileName = v_FileName
        self.Verbose = v_Verbose

    def find_section(self, v_Section):
        """
        find_section(v_Section) -> Return section line number in
        the parameters files
        """
        bFounded = False
        nLineCnt = 0
        ParamFile = open(self.FileName, "r")
        for sLine in ParamFile:
            nLineCnt += 1
            sLine = sLine.strip()
            if (len(sLine) > 0 and (not (sLine[0] == "#"))
                and (not (sLine[0:2] == "//"))):
                if ((sLine == v_Section) or (sLine[1: -1] == v_Section)):
                    bFounded = True
                    break
        ParamFile.close()

        if (bFounded):
            return (nLineCnt)
        else:
            return (0)

    def find_parameter(self, v_Section, v_Parameter):
        """
        find_parameter(v_Section, v_Parameter) -> Return
        the parameter value for the section in the parameters files
        """
        nSectionStart = self.find_section(v_Section)
        if (nSectionStart != 0):
            sParamValue = ''
            bFounded = False
            nLineCnt = 0

            ParamFile = open(self.FileName, "r")
            for sLine in ParamFile:
                sLine = sLine.strip()
                nLineCnt += 1

                if (nLineCnt < (nSectionStart + 1)):
                    continue

                if (len(sLine) > 0 and (not (sLine[0] == "#"))
                    and (not (sLine[0:2] == "//"))):

                    # If next section is founded, then no param was founded.
                    if (sLine[0] == '['):
                        break

                    if ('=' in sLine):
                        sParamName = sLine.split('=')[0].strip()
                        sParamValue = sLine.split('=')[1].strip()
                        if (sParamName == v_Parameter):
                            bFounded = True
                            break
            ParamFile.close()

            if (bFounded):
                sReturn = sParamValue
                sReturn = sReturn.split("#")[0]
                # sReturn = sReturn.split("//")[0]
                if ((sReturn[0] == '"') and (sReturn[-1] == '"')):
                    sReturn = sReturn[1:-1]
                if ((sReturn[0] == "'") and (sReturn[-1] == "'")):
                    sReturn = sReturn[1:-1]
                sReturn = sReturn.strip()
                return sReturn
            else:
                if (self.Verbose):
                    print ("\nParameter '%s' not founded for Section '%s'!\n" %
                           (v_Parameter, v_Section))
                return (-1)
        else:
            if (self.Verbose):
                print ("\nSection '%s' not founded!\n" % (v_Section))
            return (-1)

    def set_parameter(self, v_Section, v_Parameter, v_Value=''):
        """
        set_parameter(v_Section, v_Parameter, v_Value) -> Return
        the new parameter value for the section in the parameters files
        """
        nSectionStart = self.find_section(v_Section)
        if (nSectionStart != 0):
            sParamValue = ''
            sNewLine = v_Parameter + ' = ' + str(v_Value)
            bFounded = False
            nLineCnt = 0

            ParamFile = open(self.FileName, "r")
            for sLine in ParamFile:
                sLine = sLine.strip()
                nLineCnt += 1

                if (nLineCnt < (nSectionStart + 1)):
                    continue

                if (len(sLine) > 0 and (not (sLine[0] == "#")) and
                   (not (sLine[0:2] == "//"))):

                    # If next section is founded, then no param was founded.
                    if (sLine[0] == '['):
                        break

                    if ('=' in sLine):
                        sParamName = sLine.split('=')[0].strip()
                        sParamValue = sLine.split('=')[1].strip()
                        if (sParamName == v_Parameter):
                            bFounded = True
                            break
            ParamFile.close()

        if (bFounded):
            ParamFile = open(self.FileName, "r")
            FullFileContents = ParamFile.readlines()
            ParamFile.close()

            del FullFileContents[nLineCnt-1]
            FullFileContents.insert(nLineCnt, sNewLine)

            ParamFile = open(self.FileName, "w")
            FullFileContents = "".join(FullFileContents)
            ParamFile.write(FullFileContents)
            ParamFile.close()

        return self.find_parameter(v_Section, v_Parameter)
