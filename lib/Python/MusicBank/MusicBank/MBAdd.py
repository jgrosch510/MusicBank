# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                              < MBAdd.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : MBAdd.py
#
# Author       : Josef Grosch
#
# Date         : 24 Set 2023
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
    print("MBAdd: RTFM")
    
    return
    #

# -----------------------------------------------------------------------
#
# returnMasterHelp
#
# -----------------------------------------------------------------------
def returnMasterHelp():

    helpList = [
        "MB add\n",
        "  --album - Add an album to the MB repository. Two additional options\n",
        "            are required.\n\n"  ,
        "      --dest - This option overrides the standard placemanet of albums\n",
        "               with a FQP (Full Qualified Path) to the designation\n",
        "               directory. This option is optional.\n\n",
        "      --src  - This options specifies the FQP to the source directory.\n",
        "               This option is manadory.\n\n",
        "      --id   - The is the Id of the user who owns the album. This controls\n",
        "               which MB tree the album is placed, i.e. the users MB tree.\n",
        "               This option is manadory.\n\n",
        "      --offical - This switch overrides the placement of the album\n",
        "                  causing the album to be placed in the official MB tree.\n\n" ,
        "  --track - Add a track to the MB repository. Two additional options\n",
        "            are required.\n\n"  ,
        "      --dest - This option overrides the standard placemanet of albums\n",
        "               with a FQP (Full Qualified Path) to the designation\n",
        "               directory. This option is optional.\n\n",
        "      --src  - This options specifies the FQP to the source directory.\n",
        "               This option is manadory.\n\n",
        "      --id   - The is the Id of the user who owns the album. This controls\n",
        "               which MB tree the album is placed, i.e. the users MB tree.\n",
        "               This option is manadory.\n\n",
        "      --offical - This switch overrides the placement of the track\n",
        "                  causing the album to be placed in the official MB tree.\n\n",
        "  --tree - Add a user tree to the MB repository. A user tree is a\n",
        "           directory tree that is layout like an official MB tree but\n",
        "           contains files owned by the user. The user tree is located\n",
        "           under MUSIC_ROOT. If the user tree does not exist it will be\n",
        "           created. The is one mandatory option, the user id.\n\n",
        "      --id - The id of the user who will own the user tree.\n\n",
        "  --user - Add a user to the MB system. There are three required options.\n\n",
        "      --email - The user's email address\n\n",
        "      --id - The user's id. This is there Linux id found in /etc/passwd.\n",
        "             See the man pages for id and passwd\n\n",
        "      --name - The user's full name as found in /etc/passwd\n\n",
        "      --offical - This optional switch marks the MB tree as the Offical\n",
        "                  tree owned by the hosting org.\n\n"
        ]    
        
    helpMsg = ''.join(helpList)

    return helpMsg
    #

# -----------------------------------------------------------------------
#
# performAction
#
# -----------------------------------------------------------------------
def performAction(pDict):
    rDict = MBC.genReturnDict('inside MBAdd.performAction')
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

        if '--offical' in key:
            pDict['offical'] = value
            continue
            
        if '--id' in key:
            pDict['id'] = value
            continue

        if '--fqp' in key:
            pDict['fqp'] = value
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
        if 'album' in pDict and not cmdDone:
            i = 1
            tmpDict = MBA.addAlbum(pDict)
            cmdDone = True

        # Track
        if 'track' in pDict and not cmdDone:
            i = 2
            tmpDict = MBTrack.addTrack(pDict)
            cmdDone = True

        # Tree
        if 'tree' in pDict and not cmdDone:
            i = 3
            tmpDict = MBTree.addTree(pDict)
            cmdDone = True

        # Id
        if 'id' in pDict and not cmdDone:
            i = 4
            tmpDict = MBU.addUser(pDict)
            cmdDone = True

        # User
        if 'user' in pDict and not cmdDone:
            i = 5
            tmpDict = MBU.addUser(pDict)
            cmdDone = True
            
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
# printArgs
#
# -----------------------------------------------------------------------
def printArgs(argv):
    print(str(argv))
    print(len(argv))

    return
    #



# -----------------------------------------------------------------------
#
# End of MBAdd.py
#
# -----------------------------------------------------------------------

    
