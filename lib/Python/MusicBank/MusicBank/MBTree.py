# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                              < MBTree.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : MBTree.py
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
#               Copyright (c) 2020 - 2023 Moose River LLC.
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
import time
import json

myhier = os.getenv('MYHIER')
gitHome = os.getenv('GIT_HOME')    
mbLibPath = os.getenv('MBLIBPATH')
sys.path.append(mbLibPath)

import MBCommon as MBC
import MBDBUtil as MBDB


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


# ----------------------------------------------------------
#
# addTree
#
# ----------------------------------------------------------
def addTree(pDict):
    rDict = MBC.genReturnDict('inside addTree')
    RS    = MBC.ReturnStatus

    if 'id' not in pDict:
        rDict['status'] = RS.NOT_FOUND
        rDict['msg'] = f"{pDict['toolName']}: The user Id was not specified."
    else:
        debug      = False
        idFound    = False
        emailFound = False
        nameFound  = False
        doIt       = True

        userId  = pDict['id']
            
        D = MBDB.connectToDB(pDict)
        cursor = D['data']['cursor']
        conn   = D['data']['conn']
    
        query = f"select * from user where user_id = '{userId}';"
        
        cursor.execute(query)
        Rows = cursor.fetchall()
        if len(Rows) <= 0:
            # User Id not found
            rDict['status'] = RS.NOT_FOUND
            rDict['msg'] = f"{pDict['toolName']}: User Id {userId} not found."
        else:
            # User Id was found
            userName   = Rows[0][7]
            userId     = Rows[0][8]
            userEmail  = Rows[0][9]

            userIdUpper = userId.upper()
            
            config = pDict['config']
            dirs   = config['dirs']
            mbRoot = dirs['mb_root']
            mbUserRoot = f"{mbRoot}/{userId}"

            mbDirs = [
                'Alpha',
                'Archive',
                'Attic',
                'Data',
                'etc'
                ]

            alphaDirs = [
                '0-9', 'A', 'B', 'C', 'D',
                'E',   'F', 'G', 'H', 'I',
                'J',   'K', 'L', 'M', 'N',
                'O',   'P', 'Q', 'R', 'S',
                'T',   'U', 'V', 'W', 'X',
                'Y',   'Z'
                ]
            
            """`
            `{
            "path": "{MUSIC_ROOT}/KMUD",
            "owner": "KMUD",
            "email": "tree@kmud.org",
            "id": "kmud",
            "creation_date": "Wed Oct  4 11:22:32 AM PDT 2023"
            }
            """

            for entry in mbDirs:
                newPath = f"{mbUserRoot}/{entry}"
                if doIt:
                    os.makedirs(newPath)
                if debug:
                    print(f"{newPath}")

            for entry in alphaDirs:
                newPath = f"{mbUserRoot}/Alpha/{entry}"
                if doIt:
                    os.makedirs(newPath)
                if debug:
                    print(f"{newPath}")

            TS = {}
            TS['path'] = f"{{MUSIC_ROOT}}/{userId}"
            TS['owner'] = userName
            TS['email'] = userEmail
            TS['id'] = userId
            TS['creation_date'] = time.strftime("%c")

            tsStr = json.dumps(TS, indent=4)
            #TreeStats.json
            statsFile = f"{mbUserRoot}/TreeStats.json"
            if doIt:
                with open(statsFile, 'w') as fh:
                    fh.write(tsStr)

            rDict['status'] = RS.OK
            rDict['msg'] = f"{pDict['toolName']}: Directory tree for {userId} created."
            
    return rDict
    # End of addTree


# ----------------------------------------------------------
#
# deleteTree
#
# ----------------------------------------------------------
def deleteTree(pDict):
    rDict = MBC.genReturnDict('inside deleteTree')
    RS    = MBC.ReturnStatus

    return rDict
    # End of deleteTree

    
# ----------------------------------------------------------
#
# listTree
#
# ----------------------------------------------------------
def listTree(pDict):
    rDict = MBC.genReturnDict('inside listTree')
    RS    = MBC.ReturnStatus

    return rDict
    # End of listTree

# ----------------------------------------------------------
#
# listTrees
#
# ----------------------------------------------------------
def listTrees(pDict):
    rDict = MBC.genReturnDict('inside listTree')
    RS    = MBC.ReturnStatus

    return rDict
    # End of listTrees

    
# ----------------------------------------------------------
#
# updateTree
#
# ----------------------------------------------------------
def updateTree(pDict):
    rDict = MBC.genReturnDict('inside updateTree')
    RS    = MBC.ReturnStatus

    return rDict
    # End of updateTree


# -----------------------------------------------------------------------
#
# End of MBTree.py
#
# -----------------------------------------------------------------------
