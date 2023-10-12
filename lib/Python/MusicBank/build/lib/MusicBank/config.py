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
import json
import toml
from MusicBank import MB_common as MBC


"""

"""

#--start constants--

__author__     = "Josef Grosch"
__copyright__  = "Copyright 2020 - 2023 Moose River, LLC."
__license__    = "BSD 3-clause"
__version__    = "0.1"
__maintainer__ = "Josef Grosch"
__email__      = "jgrosch@gmail.com"
__status__     = "Development"

#--end constants--

# -----------------------------------------------------------------------
#
# main
#
# -----------------------------------------------------------------------
"""
def main(argv):
    RS    = MBC.ReturnStatus
    pDict = {}
    debug = False
    
    argc = len(argv)

    if debug:
        checkEnv(argv)
        
    if argc == 1:
        printMasterHelp()

    # Add    - MBAdd.py
    # Check  - MBCheck.py
    # Delete - MBDelete.py
    # List   - MBList.py
    # Manage - MBManage.py
    # Rip    - MBRip.py
    # Update - MBUpdate.py
    
    sys.exit(0)
"""    
    # End of main

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
    
    return rDict
    #

# -----------------------------------------------------------------------
#
# readConfigFile
#
# -----------------------------------------------------------------------
def readConfigFile(cDict):
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
    
    return
    # End of readConfigFile
    
# -----------------------------------------------------------------------
#
# checkEnv
#
# -----------------------------------------------------------------------
def checkEnv(cDict):
    rDict = MBC.genReturnDict('inside MBConfig.checkEnv')
    RS    = MBC.ReturnStatus

    D = {}
    outList = []
    
    # MUSIC_ROOT
    tmpEnv = os.getenv('MUSIC_ROOT')
    if tmpEnv is None:
        D['MUSIC_ROOT'] = ''
        outList.append(f"Env variable MUSIC_ROOT NOT set.\n") 
    else:
        D['MUSIC_ROOT'] = tmpEnv
        if not os.path.exists(D['MUSIC_ROOT']):
            os.makedirs(D['MUSIC_ROOT'])
        outList.append(f"Env variable MUSIC_ROOT set to {tmpEnv}.\n") 
        
    # MUSIC_TMP
    tmpEnv = os.getenv('MUSIC_TMP')
    if tmpEnv is None:
        D['MUSIC_TMP'] = ''
        outList.append(f"Env variable MUSIC_TMP NOT set.\n") 
    else:
        D['MUSIC_TMP'] = tmpEnv
        if D['MUSIC_TMP'] is not None:
            if not os.path.exists(D['MUSIC_TMP']):
                os.makedirs(D['MUSIC_TMP'])
            outList.append(f"Env variable MUSIC_TMP set to {tmpEnv}.\n") 
                
        else:
            D['MUSIC_TMP'] = '/tmp/MUSIC_TMP'
            if not os.path.exists(D['MUSIC_TMP']):
                os.makedirs(D['MUSIC_TMP'])
            outList.append(f"Env variable MUSIC_TMP set to {tmpEnv}.\n") 

    # MYHIER
    tmpEnv = os.getenv('MYHIER')
    if tmpEnv is None:
        D['MYHIER'] = ''
        outList.append(f"Env variable MYHIER NOT set.\n") 
    else:
        D['MYHIER'] = tmpEnv
        if not os.path.exists(tmpEnv):
            outList.append(f"MYHIER is set but the directory, {tmpEnv}, is not found.\n")
        else:
            outList.append(f"Env variable MYHIER set to {tmpEnv}.\n")
    
    # GIT_HOME
    tmpEnv = os.getenv('GIT_HOME')
    if tmpEnv is None:
        D['GIT_HOME'] = ''
        outList.append(f"Env variable GIT_HOME NOT set.\n") 
    else:
        D['GIT_HOME'] = tmpEnv
        if not os.path.exists(tmpEnv):
            outList.append(f"GIT_HOME is set but the directory, {tmpEnv}, is not found.\n")
        else:
            outList.append(f"Env variable GIT_HOME set to {tmpEnv}.\n") 

    outMsg = ''.join(outList)
    
    rDict['status'] = RS.OK
    rDict['msg']    = outMsg
    rDict['data']   = D
    
    return rDict
    # End of checkEnv

# -----------------------------------------------------------------------
#
# entry point
#
# -----------------------------------------------------------------------
#if __name__ == '__main__':
#    main(sys.argv, len(sys.argv))

    
# -----------------------------------------------------------------------
#
# End of MBConfig.py
#
# -----------------------------------------------------------------------
