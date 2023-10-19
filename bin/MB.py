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

mbLibPath = os.getenv('MBLIBPATH')
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

    rDict = MBU.parseArgs(argv, argc)
    cDict['argsList'] = rDict['data']
    
    rDict = MBConfig.performAction(cDict)
    
    selectedTool = argv[1].lower()
    if selectedTool in Tools:

        # Add
        if 'add' in selectedTool:
            j = 0
            import MBAdd as MBA
            cDict['action'] = 'add'
            rDict = MBA.performAction(cDict)
        # Backup
        elif 'backup' in selectedTool:
            j = 1
            import MBBackup
            cDict['action'] = 'backup'
            rDict = MBBackup.performAction(cDict)
        # Check
        elif 'check' in selectedTool:
            j = 2
            import MBCheck
            cDict['action'] = 'check'
            rDict = MBCheck.performAction(cDict)
        # Config
        elif 'config' in selectedTool:
            j = 3
            cDict['action'] = 'config'
            if not cDict['done']:
                rDict = MBConfig.performAction(cDict)
            outStr = MBConfig.genConfigMsg(cDict)
            rDict['msg'] = outStr
        # Delete
        elif 'delete' in selectedTool:
            j = 4
            import MBDelete
            cDict['action'] = 'delete'
            rDict = MBDelete.performAction(cDict)
        # Fis
        elif 'fix' in selectedTool:
            j = 5
            import MBFix
            cDict['action'] = 'fix'
            rDict = MBFix.performAction(cDict)
        # Help
        elif 'help' in selectedTool:
            j = 6
            cDict['action'] = 'help'
            rDict = returnMasterHelp()
        # List
        elif 'list' in selectedTool:
            j = 7
            import MBList
            cDict['action'] = 'list'
            rDict = MBList.performAction(cDict)
        # Manage
        elif 'manage' in selectedTool:
            j = 8
            import MBManage
            cDict['action'] = 'manage'
            rDict = MBManage.performAction(cDict)
        # Merge
        elif 'merge' in selectedTool:
            j = 9
            import MBMerge
            cDict['action'] = 'merge'
            rDict = MBMerge.performAction(cDict)
        # Move
        elif 'move' in selectedTool:
            j = 10
            import MBMove
            cDict['action'] = 'move'
            rDict = MBMove.performAction(cDict)
        # Rip
        elif 'rip' in selectedTool:
            j = 11
            import MBRip
            cDict['action'] = 'rip'
            rDict = MBRip.performAction(cDict)
        # Remove
        elif 'remove' in selectedTool:
            j = 12
            import MBRemove
            cDict['action'] = 'remove'
            rDict = MBRemove.performAction(cDict)
        # Update
        elif 'update' in selectedTool:
            j = 13
            import MBUpdate
            cDict['action'] = 'update'
            rDict = MBUpdate.performAction(cDict)
        else:
            print(f"Error: {selectedTool} not a legal option") 

    j = 14
    
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
        "* Update -\n\n"
        ]

    outStr = ''.join(Lines)

    rDict['status'] = RS.OK
    rDict['msg']    = outStr

    return rDict
    # End of printMasterHelp

    
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
