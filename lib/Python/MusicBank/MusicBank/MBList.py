# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                              < MBList.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : MBList.py
#
# Author       : Josef Grosch
#
# Date         : 26 Sep 2023
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

import MBCommon as MBC
import MBUser as MBU
import MBUtil as MBUT
import MBAlbum as MBA
import MBTree
import MBTrack


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
def performAction(pDict):
    rDict = MBC.genReturnDict('inside MBList.performAction')
    RS    = MBC.ReturnStatus

    argv     = pDict['argv']
    argc     = pDict['argc']
    config   = pDict['config']
    action   = pDict['action']
    argsList = pDict['argsList']
            
    helpFound = False
    debug = False
    if debug:
        print(str(argv))
        print(len(argv))
        
    for entry in argsList:
        index = entry['index']
        key   = entry['key']
        value = entry['value']

        if 'calling program' in value:
            continue

        if 'cmd' in value:
            continue

        if 'skip' in value:
            continue

        if '--album' in key:
            pDict['album'] = value
            continue
            
        if '--track' in key:
            pDict['track'] = value
            continue
            
        if '--tree' in key:
            pDict['tree'] = value
            continue
            
        if '--user' in key:
            pDict['user'] = value
            continue

        if '--offical' in key:
            pDict['offical'] = value
            continue
            
        if '--id' in key:
            pDict['id'] = value
            continue

        if '--email' in key:
            pDict['email'] = value
            continue

        if '--name' in key:
            pDict['name'] = value
            continue

        if '--help' in key:
            msg = returnMasterHelp()
            helpFound = True
            break
    
    i = 0
    
    if helpFound == False:
        # Album
        if 'album' in pDict:
            i = 1
            tmpDict = MBA.listAlbums(pDict)

        # Track
        if 'track' in pDict:
            i = 2
            tmpDict = MBTrack.listTracks(pDict)

        # Tree
        if 'tree' in pDict:
            i = 3
            tmpDict = MBTree.listTrees(pDict)

        # Id
        if 'id' in pDict:
            i = 4
            tmpDict = MBU.listUser(pDict)

        # User
        if 'user' in pDict:
            i = 5
            tmpDict = MBU.listUsers(pDict)
            
        rDict['status'] = tmpDict['status']
        rDict['msg'] = tmpDict['msg']
    else:
        # --help found. Return help
        rDict['msg'] = msg
        rDict['status'] = RS.OK
        
    return rDict
    #

# -----------------------------------------------------------------------
#
# returnMasterHelp
#
# -----------------------------------------------------------------------
def returnMasterHelp():
    helpMsg = 'RTFM'
    
    return helpMsg

# -----------------------------------------------------------------------
#
# End of MBList.py
#
# -----------------------------------------------------------------------
