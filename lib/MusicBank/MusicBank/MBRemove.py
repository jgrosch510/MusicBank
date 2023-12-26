# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                             < MBRomove.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : MBRomove.py
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


def printMasterHelp():
    print("RTFM")

    return

def performAction(argv):
    print(str(argv))
    print(len(argv))

    return
    #


# -----------------------------------------------------------------------
#
# End of MBRomove.py
#
# -----------------------------------------------------------------------
