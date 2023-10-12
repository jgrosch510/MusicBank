# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                              < util.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : util.py
#
# Author       : Josef Grosch
#
# Date         : 08 Sep 2023
#
# Version      : 0.1
#
# Modification : I guess
#
# Application  :
#
# Description  :
#
# Notes        :
#
# Functions    :
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
#                              Copyright
#
#                   Copyright (c) 2023 Moose River LLC.
#                           <jgrosch@gmail.com>
#
#                         All Rights Reserved
#
#               Deadicated to my brother Jerry Garcia,
#            who passed from this life on August 9, 1995.
#                     Happy trails to you, Jerry
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
#                               GPG Key
#
# pub rsa4096 2022-01-22 [SC] [expires: 2024-01-22]
# Key fingerprint = D360ABF3C34858F617FC6C8887FE74CD0D56DFE2
# uid Josef Grosch <jgrosch@gmail.com>
# sub rsa4096 2022-01-22 [E] [expires: 2024-01-22]
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
#                         Contact Information
#
#                          Moose River LLC.
#                            P.O. Box 9403
#                         Berkeley, Ca. 94709
#
#                      http://www.mooseriver.com
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# Import
#
# -----------------------------------------------------------------------
import os, sys

myhier = os.getenv('MYHIER')
gitHome = os.getenv('GIT_HOME')    
mbLibPath = os.getenv('MBLIBPATH')
sys.path.append(mbLibPath)

import json
import audio_metadata
import MBCommon as MBC

#--start constants--

__author__      = "Josef Grosch"
__copyright__   = "Copyright 2023 Moose River, LLC."
__description__ = "This tool manages the MusicBank tree"
__email__       = "jgrosch@gmail.com"
__license__     = "BSD 3-clause"
__maintainer__  = "Josef Grosch"
__status__      = "Development"
__version__     = "0.1"

#--end constants--

"""
util  --  functions related to the DB table, util
"""



# ----------------------------------------------------------
#
# toJson
#
# ----------------------------------------------------------
def toJson(pDict):
    rDict = MBC.genReturnDict('inside toJson')
    RS    = MBC.ReturnStatus

    jObj = json.dumps(pDict, indent=4)
    rDict['data'] = jObj
    
    return rDict
    # End of toJson

# --------------------------------------------------------------------
#
# genFfpFile
#
# --------------------------------------------------------------------
def genFfpFile(path):
    RS = MBC.ReturnStatus
    rDict = MBC.genReturnDict('inside genFfFile')


    if os.path.exists(path):
        statusCode = RS.OK
    else:
        statusCode = RS.NOT_FOUND
        rDict['status'] = statusCode
        rDict['msg'] = f"ERROR: path {path} NOT found."

    if statusCode == RS.OK:
        flacList = []
        ffpLines = []

        bits = path.split('/')
        bitsCount = len(bits)
        albumIndex = (bitsCount - 1)
        albumName = bits[albumIndex]
    
        for root,d_names,f_names in os.walk(path):
            r = root
            Dirs = d_names
            Files = f_names

            if len(Files) > 0:
                for entry in Files:
                    if entry.endswith('.flac'):
                        flacList.append(f"{root}/{entry}")
                    # End of if
                # End of for loop
            # End of if
        # End of for loop

        for entry in flacList:
            m = audio_metadata.load(entry)
            md5 = m['streaminfo']['md5']
            
            bits = entry.split('/')
            bitsCount = len(bits)
            fileIndex = (bitsCount - 1)
            fileName = bits[fileIndex]
            tmpStr = f"{fileName}:{md5}\n"
            ffpLines.append(tmpStr)
        # End of for loop
    
        ffpLines.sort()
        outStr = ''.join(ffpLines)
        ffpFileName = f"{path}/{albumName}.ffp"
        with open(ffpFileName, 'w') as fh:
            fh.write(outStr)

            rDict['status'] = RS.OK
            rDict['msg'] = f"FFP file {ffpFileName} created"
    
    return rDict
    # End of genFfpFile

# --------------------------------------------------------------------
#
# parseArgs
#
# --------------------------------------------------------------------
def parseArgs(argv, argc):
    rDict = MBC.genReturnDict('inside MBList.performAction')
    RS    = MBC.ReturnStatus

    T2 = MBC.Tools()
    Tools = T2.Tools
    ToolsTest = MBC.Tools().Tools
    
    D = {}
    argList = []
    index = 0

    for entry in argv:
        D['index'] = index
        D['key']   = entry
        D['value'] = ''
        argList.append(D)
        index += 1
        D = {}

    for entry in argList:
        index = entry['index']
        key   = entry['key']
        value = entry['value']

        nextIndex = (index + 1)
        
        if index == 0:
            entry['value'] = 'calling program'
            continue

        if index == 1:
            if key in Tools:
                entry['value'] = 'cmd'
                continue
            
        if key.startswith('--'):
            if nextIndex < argc:
                if argList[nextIndex]['key'].startswith('--'):
                    entry['value'] = 'true'
                else:
                    entry['value'] = argList[nextIndex]['key']
            else:
                entry['value'] = 'true'
        else:
            entry['value'] = 'skip'
                
    j = 0
    rDict['status'] = RS.OK
    rDict['msg']    = 'arg list parsed'
    rDict['data']   = argList
    
    return rDict
    # End of parseArgs

# -----------------------------------------------------------------------
#
# End of util.py
#
# -----------------------------------------------------------------------
