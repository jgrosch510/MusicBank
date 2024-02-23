# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                             < MBDelete.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : MBDelete.py
#
# Author       : Josef Grosch
#
# Date         : 17 Nov 2019
#
# Version      : 0.0
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
#               Copyright (c) 2020 - 2024 Moose River LLC.
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
import MBUser
import MBUtil
import MBAlbum
import MBTree
import MBTrack

#--start constants--

__author__     = "Josef Grosch"
__copyright__  = "Copyright 2020 - 2024 Moose River, LLC."
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
# returnMasterHelp
#
# -----------------------------------------------------------------------
def returnMasterHelp():
    helpList = [
        "MB delete\n",
        "  --album - \n",
        "  --email - \n",
        "  --id - \n",
        "  --name - \n",
        "  --offical - \n",
        "  --track - \n",
        "  --tree - \n",
        "  --users - \n",
        "  --help - This message\n"
        ]

    helpMsg = ''.join(helpList)
    
    return helpMsg
    # End of returnMasterHelp

# -----------------------------------------------------------------------
#
# perfoemAction
#
# -----------------------------------------------------------------------
def performAction(pDict):
    rDict = MBC.genReturnDict('inside MBDelete.performAction')
    RS    = MBC.ReturnStatus

    argv     = pDict['argv']
    argc     = pDict['argc']
    config   = pDict['config']
    action   = pDict['action']
    argsList = pDict['argsList']

    helpFound = False
    cmdDone = False
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
    # End of for loop

    
    i = 0
    
    if helpFound == False:
        # Album
        if 'album' in pDict and not cmdDone:
            i = 0
            tmpDict = MBAbum.deleteAlbum(pDict)
            cmdDone = True

        # Track
        if 'track' in pDict and not cmdDone:
            i = 0
            tmpDict = MBTrack.deleteTrack(pDict)
            cmdDone = True

        # Tree
        if 'tree' in pDict and not cmdDone:
            i = 0
            tmpDict = MBTree.deleteTree(pDict)
            cmdDone = True

        # User
        if 'user' in pDict and not cmdDone:
            i = 0
            tmpDict = MBUser.deleteUser(pDict)
            cmdDone = True

        # Id
        if 'id' in pDict and not cmdDone:
            i = 0
            tmpDict = MBUser.deleteUser(pDict)
            cmdDone = True
            
        rDict['status'] = tmpDict['status']
        rDict['msg'] = tmpDict['msg']
    else:
        # --help found. Return help
        rDict['msg'] = msg
        rDict['status'] = RS.OK
    
    return rDict

        
    return
    #


    

# -----------------------------------------------------------------------
#
# End of MBDelete.py
#
# -----------------------------------------------------------------------
