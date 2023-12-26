# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                              < MBConfig.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : MBConfig.py
#
# Author       : Josef Grosch
#
# Date         : 25 Sep 2023
#
# Version      : 0.1
#
# Modification : Some
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
#               Copyright (c) 2020 - 2023 Moose River LLC.
#                           <jgrosch@gmail.com>
#
#                         All Rights Reserved
#
#                 Deadicated to my brother Jerry Garcia,
#              who passed from this life on August 9, 1995.
#                       Happy trails to you, Jerry
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
#                               GPG Key
#
# pub  rsa4096 2022-01-22 [SC] [expires: 2024-01-22]
# Key  fingerprint - D360 ABF3 C348 58F6 17FC 6C88 87FE 74CD 0D56 DFE2
# uid  [ultimate] Josef Grosch <jgrosch@gmail.com>
# sub  rsa4096 2022-01-22 [E] [expires: 2024-01-22]
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
import toml
import MBCommon as MBC

#--start constants--

__author__     = "Josef Grosch"
__copyright__  = "Copyright 2020 - 2023 Moose River, LLC."
__license__    = "BSD 3-clause"
__version__    = "0.1"
__maintainer__ = "Josef Grosch"
__email__      = "jgrosch@gmail.com"
__status__     = "Development"

#--end constants--


"""

"""



# -----------------------------------------------------------------------
#
# printMasterHelp
#
# -----------------------------------------------------------------------
def printMasterHelp():
    print("RTFM")

    return

# -----------------------------------------------------------------------
#
# performAction
#
# -----------------------------------------------------------------------
def performAction(cDict):
    rDict = readConfigFile(cDict)
    rDict = checkEnv(rDict)
    cDict['env'] = rDict['data']
    cDict['done'] = True
    
    return rDict
    #

# -----------------------------------------------------------------------
#
# readConfigFile
#
# -----------------------------------------------------------------------
def readConfigFile(cDict):
    rDict = MBC.genReturnDict('inside MBConfig.readConfigFile')
    RS    = MBC.ReturnStatus

    baseDir = '/usr/local/site/MusicBank/etc'
    inFile = f"{baseDir}/MusicBank.conf"
    
    userHome = cDict['HOME']
    userConfig = f"{userHome}/.config/MusicBank/MusicBank.conf"
    
    with open(inFile, 'r') as fh:
        Lines = fh.read()
    sc = toml.loads(Lines)

    if os.path.exists(userConfig):
        with open(userConfig, 'r') as fh:
            Lines = fh.read()
        uc = toml.loads(Lines)

        for entry in sc:
            if entry in uc:
                scEntry = sc[entry]
                ucEntry = uc[entry]
                for key in scEntry:
                    scValue = scEntry[key]
                    ucValue = ucEntry[key]
                    if scValue.lower() == ucValue.lower():
                        continue
                    else:
                        scEntry[key] = ucValue
                    # End of if/else
                # End of for loop
            # End of if
        # End of for loop
    # End of if
                    
    cDict['config'] = sc
    rDict['status'] = RS.OK
    rDict['data'] = sc
    
    return rDict
    # End of readConfigFile
    
# -----------------------------------------------------------------------
#
# checkEnv
#
# -----------------------------------------------------------------------
def checkEnv(cDict):
    rDict = MBC.genReturnDict('inside MBConfig.checkEnv')
    RS    = MBC.ReturnStatus

    Env = {}
    outList = []
    
    # MUSIC_ROOT
    tmpEnv = os.getenv('MUSIC_ROOT')
    if tmpEnv is None:
        Env['MUSIC_ROOT'] = ''
        outList.append(f"Env variable MUSIC_ROOT NOT set.\n") 
    else:
        Env['MUSIC_ROOT'] = tmpEnv
        if not os.path.exists(Env['MUSIC_ROOT']):
            os.makedirs(Env['MUSIC_ROOT'])
        outList.append(f"Env variable MUSIC_ROOT set to {tmpEnv}.\n") 
        
    # MUSIC_TMP
    tmpEnv = os.getenv('MUSIC_TMP')
    if tmpEnv is None:
        Env['MUSIC_TMP'] = '/usr/tmp/MusicBank'
        outList.append(f"Env variable MUSIC_TMP NOT set.\n") 
    else:
        Env['MUSIC_TMP'] = tmpEnv
        if Env['MUSIC_TMP'] is not None:
            if not os.path.exists(Env['MUSIC_TMP']):
                os.makedirs(Env['MUSIC_TMP'])
            outList.append(f"Env variable MUSIC_TMP set to {tmpEnv}.\n") 
                
        else:
            Env['MUSIC_TMP'] = '/tmp/MUSIC_TMP'
            if not os.path.exists(Env['MUSIC_TMP']):
                os.makedirs(Env['MUSIC_TMP'])
            outList.append(f"Env variable MUSIC_TMP set to {tmpEnv}.\n") 

    # MYHIER
    tmpEnv = os.getenv('MYHIER')
    if tmpEnv is None:
        Env['MYHIER'] = ''
        outList.append(f"Env variable MYHIER NOT set.\n") 
    else:
        Env['MYHIER'] = tmpEnv
        if not os.path.exists(tmpEnv):
            outList.append(f"MYHIER is set but the directory, {tmpEnv}, is not found.\n")
        else:
            outList.append(f"Env variable MYHIER set to {tmpEnv}.\n")
    
    # GIT_HOME
    tmpEnv = os.getenv('GIT_HOME')
    if tmpEnv is None:
        Env['GIT_HOME'] = ''
        outList.append(f"Env variable GIT_HOME NOT set.\n") 
    else:
        Env['GIT_HOME'] = tmpEnv
        if not os.path.exists(tmpEnv):
            outList.append(f"GIT_HOME is set but the directory, {tmpEnv}, is not found.\n")
        else:
            outList.append(f"Env variable GIT_HOME set to {tmpEnv}.\n") 

    # MBLIBPATH
    tmpEnv = os.getenv('MBLIBPATH')
    if tmpEnv is None:
        Env['MBLIBPATH'] = ''
        outList.append(f"Env variable MBLIBPATH NOT set.\n") 
    else:
        Env['MBLIBPATH'] = tmpEnv
    
    # MB_USER_ID
    tmpEnv = os.getenv('MB_USER_ID')
    if tmpEnv is None:
        Env['MB_USER_ID'] = ''
        outList.append(f"Env variable MB_USER_ID NOT set.\n") 
    else:
        Env['MB_USER_ID'] = tmpEnv

    # MB_USER_NAME
    tmpEnv = os.getenv('MB_USER_NAME')
    if tmpEnv is None:
        Env['MB_USER_NAME'] = ''
        outList.append(f"Env variable MB_USER_NAME NOT set.\n") 
    else:
        Env['MB_USER_NAME'] = tmpEnv

    # MB_USER_EMAIL
    tmpEnv = os.getenv('MB_USER_EMAIL')
    if tmpEnv is None:
        Env['MB_USER_EMAIL'] = ''
        outList.append(f"Env variable MB_USER_EMAIL NOT set.\n") 
    else:
        Env['MB_USER_EMAIL'] = tmpEnv
    
    outMsg = ''.join(outList)
    
    rDict['status'] = RS.OK
    rDict['msg']    = outMsg
    rDict['data']   = Env
    
    return rDict
    # End of checkEnv


# -----------------------------------------------------------------------
#
# genConfigMsg
#
# -----------------------------------------------------------------------
def genConfigMsg(pDict):
    outStr = ''

    cJson = json.dumps(pDict['config'], indent=4)
    eJson = json.dumps(pDict['env'], indent=4)
    outStr = f"MB config:\nConfig:\n{cJson}\n\nEnv:\n{eJson}\n"

    return outStr
    # End of genConfigMsg

    
# -----------------------------------------------------------------------
#
# End of MBConfig.py
#
# -----------------------------------------------------------------------
