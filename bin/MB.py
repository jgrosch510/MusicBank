#!/usr/bin/env python
# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                                < MB.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : MB.py
#
# Author       : Josef Grosch
#
# Date         : 01 Set 2023
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
import json
import importlib

mbLibPath = os.getenv('MBLIBPATH')
if mbLibPath == None:
    print('ERROR: MBLIBPATH NOT set
sys.path.append(mbLibPath)

import MBCommon as MBC
import MBUtil as MBU
import MBConfig

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
MB - master controller
"""


# -----------------------------------------------------------------------
#
# main
#
# -----------------------------------------------------------------------
def main(argv, argc):    
    RS = MBC.ReturnStatus

    T2 = MBC.Tools()
    Tools = T2.Tools

    # cDict - Config Dictonary
    # pDict - Parameter Dictonary
    # rDict - Return Dictonary
    
    cDict = {} 

    cDict['argv'] = argv
    cDict['argc'] = argc
    if argc == 1:
        printMasterHelp()
        sys.exit(RS.OK)
        
    cDict['HOME']         = os.getenv('HOME')
    cDict['toolName']     = argv[0].replace('./', '')
    cDict['selectedTool'] = argv[1].lower()
    cDict['myhier']       = os.getenv('MYHIER')
    cDict['gitHome']      = os.getenv('GIT_HOME')    

    rDict = MBU.parseArgs(cDict)
    rDict = MBConfig.performAction(cDict)
    cmdDict = loadCmdDict()
    
    selectedTool = cDict['selectedTool']
    cDict['action'] = selectedTool

    if 'help' in selectedTool:
        rDict = returnMasterHelp()
    else:
        if selectedTool in Tools:
            moduleName = cmdDict[selectedTool]['module']
            MBEX = importlib.import_module(moduleName)
        else:
            print(f"Error: {selectedTool} not a legal option") 

        if 'config' in selectedTool:
            if not cDict['done']:
                rDict = MBEX.performAction(cDict)
            outStr = MBEX.genConfigMsg(cDict)
            rDict['msg'] = outStr
        else:
            rDict = MBEX.performAction(cDict)
        
    if rDict['status'] == RS.OK:
        print(f"{rDict['msg']}\n")
        if 'list' in cDict['action'] and len(rDict['data']) > 0:
            print(f"{rDict['data']}\n")
    else:
        print("\n")
        print(rDict['msg'])
        
        
    sys.exit(RS.OK)
    # End of main

    
# -----------------------------------------------------------------------
#
# printMasterHelp
#
# -----------------------------------------------------------------------
def printMasterHelp():
    rDict = returnMasterHelp()
    outStr = rDict['msg']
    print(outStr)

    return
    # End of printMasterHelp


# -----------------------------------------------------------------------
#
# returnMasterHelp
#
# -----------------------------------------------------------------------
def returnMasterHelp():
    rDict = MBC.genReturnDict('inside MB.returnMasterHelp')
    RS    = MBC.ReturnStatus

    Lines = [
        "MB.py: ",
        "This controller has eight commands that handle a MusicBank repository. The\n",
        "command are Add, Check, Config, Delete, Fix, List, Merge, Move, and Update.\n\n",
        "* Add - Add an album, a track, a user, or a user tree to the MB repisoroty\n\n",
        "* Check - Check the \"correctness\" of a track, an album, of a tree\n\n",
        "* Config - Output the current config\n\n",
        "* Delete - Delete a user, a track, an album or a tree. Note. Deleting a\n",
        "           user also deletes all items owned by the user.\n\n",
        "* Fix - \n\n",
        "* List - List either users or albums\n\n",
        "* Merge - Merge 2 trees into a new tree\n\n", 
        "* Move - Move an album or track from one tree to another\n\n",
        "* Rip - Rip a CD and place the music files in a spefied tree\n\n",
        "* Update -\n\n"
        ]

    outStr = ''.join(Lines)

    rDict['status'] = RS.OK
    rDict['msg']    = outStr

    return rDict
    # End of printMasterHelp

def loadCmdDict():
    cmdDict = {
        'add': {
            'module':'MBAdd',
            'index': 1
            },
        'backup': {
            'module':'MBBackup',
            'index': 1
            },
        'check': {
            'module':'MBBheck',
            'index': 1
            },
        'config': {
            'module':'MBConfig',
            'index': 1
            },
        'delete': {'module':'MBDelete', 'index': 1},
        'fix': {'module':'MBFix', 'index': 1},
        'help': {'module':'MBHelp', 'index': 1},
        'list': {'module':'MBList', 'index': 1},
        'manage': {'module':'MBManage', 'index': 1},
        'merge': {'module':'MBMerge', 'index': 1},
        'move': {'module':'MBMove', 'index': 1},
        'rip': {'module':'MBRip', 'index': 1},
        'remove': {'module':'MBRemove', 'index': 1},
        'update': {'module':'MBUpdate', 'index': 1}
        }
    """
    cmdDict = {}
    
    cmdDict['add'] = 'MBAdd'
    cmdDict['backup'] = 'MBBackup'
    cmdDict['check'] = 'MBBheck'
    cmdDict['config'] = 'MBConfig'
    cmdDict['delete'] = 'MBDelete'
    cmdDict['fix'] = 'MBFix'
    cmdDict['help'] = 'MBHelp'
    cmdDict['list'] = 'MBList'
    cmdDict['manage'] = 'MBManage'
    cmdDict['merge'] = 'MBMerge'
    cmdDict['move'] = 'MBMove'
    cmdDict['rip'] = 'MBRip'
    cmdDict['remove'] = 'MBRemove'
    cmdDict['update'] = 'MBUpdate'
    """
    return cmdDict
    # End of loadCmdDict
    
# -----------------------------------------------------------------------
#
# Entry Point
#
# -----------------------------------------------------------------------
if __name__ == '__main__':
    main(sys.argv, len(sys.argv))

    
# -----------------------------------------------------------------------
#
# End of MB.py
#
# -----------------------------------------------------------------------
