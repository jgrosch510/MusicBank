# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                              < user.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : user.py
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
import json
import sqlite3
import time

from MusicBank import common as MBC
from MusicBank import db_util as MBDB

"""
user  --  functions related to the DB table, user
"""

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


# ----------------------------------------------------------
#
# addUser
#
# ----------------------------------------------------------
def addUser(pDict):
    rDict = MBC.genReturnDict('inside addUser')
    RS    = MBC.ReturnStatus

    userName  = pDict['user']
    userEmail = pDict['email']

    D = MBDB.connectToDB(pDict)
    cur  = D['data']['cur']
    conn = D['data']['conn']
    
    query = f"select * from user where user_name = '{userName}';"
        
    cur.execute(query)
    Rows = cur.fetchall()
    if len(Rows) >= 1:
        rDict['status'] = RS.NOT_OK
        rDict['msg'] = f"ERROR: User {userName} found. User name must be unique."
    else:
        active = 'YES'
        epoch   = int(time.time())
        now = time.strftime("%c")

        if userName is None:
            userName = ""

        if userEmail is None:
            userEmail = ""
                    
        query = ("insert into user (insert_date, insert_epoch, active, "
                 "user_name, user_email) values ('{}', '{}', '{}', '{}', '{}');"
                 .format(now, epoch, active, userName, userEmail))

        cur.execute(query)
        value = cur.lastrowid
        if value >= 1:
            rDict['status'] = RS.OK
            rDict['msg'] = "New user DB record inserted"
                         
    # End of else

    conn.commit()
    cur.close()
    
    return rDict
    # End of addUser


# ----------------------------------------------------------
#
# deleteUser
#
# ----------------------------------------------------------
def deleteUser(pDict):
    rDict = MBC.genReturnDict('inside deleteUser')
    RS    = MBC.ReturnStatus

    D = MBDB.connectToDB(pDict)
    cur  = D['data']['cur']
    conn = D['data']['conn']
    
    userName = pDict['args'].user
    userEmail = pDict['args'].email

    # delete from user where user_name = 'bdobbs';
    query = f"delete from user where user_name = '{userName}';"

    cur.execute(query)
    value = cur.lastrowid
    if value >= 1:
        rDict['status'] = RS.OK
        rDict['msg'] = f"User {userName} deleted"

    conn.commit()
    cur.close()
    
    return rDict
    # End of deleteUser

    
# ----------------------------------------------------------
#
# listUser
#
# ----------------------------------------------------------
def listUser(pDict):
    rDict = MBC.genReturnDict('inside listUser')
    RS    = MBC.ReturnStatus
    UT    = MBC.UserTable
    
    JL = []
    UD = {}
    D = MBDB.connectToDB(pDict)
    cur  = D['data']['cur']
    conn = D['data']['conn']
    
    query = 'select * from user'
    cur.execute(query)
    Rows = cur.fetchall()
    if len(Rows) > 0:
        for row in Rows:
            UD['recNum']      = row[UT.REC_NUM]
            UD['insertDate']  = row[UT.INSERT_DATE]
            UD['insertEpoch'] = row[UT.INSERT_EPOCH]
            UD['active']      = row[UT.ACTIVE]
            UD['userName']    = row[UT.USER_NAME]
            UD['userEmail']   = row[UT.USER_EMAIL]
            JL.append(UD)
            UD = {}
        # End of for loop
            
        rDict['status'] = RS.OK
        rDict['msg']    = 'Users found'
        rDict['data']   = JL
    else:
        rDict['status'] = RS.NOT_FOUND
        rDict['msg'] = 'No users found'
    # End of if/else

    conn.commit()
    cur.close()

    return rDict
    # End of listUser

    
# ----------------------------------------------------------
#
# updateUser
#
# ----------------------------------------------------------
def updateUser(pDict):
    rDict = MBC.genReturnDict('inside updateUser')
    RS    = MBC.ReturnStatus

    return rDict
    # End of updateUser


# -----------------------------------------------------------------------
#
# End of user.py
#
# -----------------------------------------------------------------------
