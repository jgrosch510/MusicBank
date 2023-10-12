# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                              < track.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : MBTrack.py
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


# ----------------------------------------------------------
#
# addTrack
#
# ----------------------------------------------------------
def addTrack(pDict):
    rDict = MBC.genReturnDict('inside addTrack')
    RS    = MBC.ReturnStatus

    return rDict
    # End of addTrack


# ----------------------------------------------------------
#
# deleteTrack
#
# ----------------------------------------------------------
def deleteTrack(pDict):
    rDict = MBC.genReturnDict('inside deleteTrack')
    RS    = MBC.ReturnStatus

    return rDict
    # End of deleteTrack

    
# ----------------------------------------------------------
#
# listTrack
#
# ----------------------------------------------------------
def listTrack(pDict):
    rDict = MBC.genReturnDict('inside listTrack')
    RS    = MBC.ReturnStatus

    return rDict
    # End of listTrack

# ----------------------------------------------------------
#
# listTracks
#
# ----------------------------------------------------------
def listTracks(pDict):
    rDict = MBC.genReturnDict('inside listTrack')
    RS    = MBC.ReturnStatus

    return rDict
    # End of listTracks

    
# ----------------------------------------------------------
#
# updateTrack
#
# ----------------------------------------------------------
def updateTrack(pDict):
    rDict = MBC.genReturnDict('inside updateTrack')
    RS    = MBC.ReturnStatus

    return rDict
    # End of updateTrack


# -----------------------------------------------------------------------
#
# End of album.py
#
# -----------------------------------------------------------------------
