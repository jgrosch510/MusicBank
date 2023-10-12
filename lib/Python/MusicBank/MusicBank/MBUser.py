# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                              < MBUser.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : MBUser.py
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
user  --  functions related to the DB table, user
"""



# ----------------------------------------------------------
#
# addUser
#
# ----------------------------------------------------------
def addUser(pDict):
    rDict = MBC.genReturnDict('inside addUser')
    RS    = MBC.ReturnStatus

    debug      = False
    idFound    = False
    emailFound = False
    nameFound  = False

    if 'id' in pDict:
        userId  = pDict['id']
        idFound = True

    if 'email' in pDict:
        userEmail = pDict['email']
        emailFound = True

    if 'name' in pDict:
        userName  = pDict['name']
        nameFound = True

        
    if idFound and emailFound and nameFound:
        D = MBDB.connectToDB(pDict)
        cursor = D['data']['cursor']
        conn   = D['data']['conn']
    
        query = f"select * from user where user_id = '{userId}';"
        
        cursor.execute(query)
        Rows = cursor.fetchall()
        if len(Rows) >= 1:
            rDict['status'] = RS.NOT_OK
            rDict['msg'] = f"ERROR: User {userName} found. User name, id, and email must be unique."
        else:
            epoch        = int(time.time())
            now          = time.strftime("%c")
            rec_version  = 1
            insert_time  = now
            insert_epoch = epoch
            update_time  = now
            update_epoch = epoch
            active       = 1
            user_name    = userName
            user_id      = userId
            user_email   = userEmail
        
            query = ("insert into user (rec_version, insert_time, insert_epoch,  "
                     "update_time, update_epoch, active, "
                     "user_name, user_id, user_email) values ({}, '{}', '{}', '{}', '{}', "
                     " {}, '{}', '{}', '{}');"
                     .format(rec_version, insert_time, insert_epoch,
                             update_time, update_epoch, active, user_name, user_id, user_email))

            if debug:
                print(query)

            cursor.execute(query)
            value = cursor.lastrowid
            if value >= 1:
                rDict['status'] = RS.OK
                rDict['msg'] = f"New user, {userId}, DB record inserted"
                         
        # End of else

        conn.commit()
        cursor.close()
    else:
        outMsg = []
        outMsg.append("MB.py add error: \n")
        
        if not idFound:
            outMsg.append("\tUser id is not specified.(--id <ID>)\n")

        if not emailFound:
            outMsg.append("\tUser email is not specified.(--email <EMAIL>)\n")

        if not nameFound:
            outMsg.append("\tUser name is not specified.(--name <NAME>)\n")

        outStr = ''.join(outMsg)

        rDict['status'] = RS.NOT_OK
        rDict['msg'] = outStr
        
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
    cursor  = D['data']['cursor']
    conn    = D['data']['conn']
    
    userId    = pDict['id']
    #userEmail = pDict['email']
    
    query = f"select * from user where user_id = '{userId}';"
    
    cursor.execute(query)
    Rows = cursor.fetchall()
    if len(Rows) <= 0:
        rDict['status'] = RS.NOT_OK
        rDict['msg'] = f"ERROR: User Id {userId} Not found."
    else:
        # delete from user where user_name = 'bdobbs';
        query = f"delete from user where user_id = '{userId}';"

        cursor.execute(query)
        value = cursor.lastrowid
        if value == 0:
            rDict['status'] = RS.OK
            rDict['msg'] = f"User Id {userId} deleted"
    # End of if/else
    
    conn.commit()
    cursor.close()
    
    return rDict
    # End of deleteUser

    
# ----------------------------------------------------------
#
# listUsers
#
# ----------------------------------------------------------
def listUsers(pDict):
    rDict = MBC.genReturnDict('inside listUser')
    RS    = MBC.ReturnStatus
    UT    = MBC.UserTable
    
    JL = []
    UD = {}
    D = MBDB.connectToDB(pDict)
    cursor  = D['data']['cursor']
    conn    = D['data']['conn']
    
    query = 'select * from user'
    cursor.execute(query)
    Rows = cursor.fetchall()
    if len(Rows) > 0:
        for row in Rows:
            UD['recNum']      = row[UT.REC_NUM]
            UD['recVersion']  = row[UT.REC_VERSION]
            UD['insertTime']  = row[UT.INSERT_TIME]
            UD['insertEpoch'] = row[UT.INSERT_EPOCH]
            UD['updateTime']  = row[UT.UPDATE_TIME]
            UD['updateEpoch'] = row[UT.UPDATE_EPOCH]
            UD['active']      = row[UT.ACTIVE]
            UD['userName']    = row[UT.USER_NAME]
            UD['userId']      = row[UT.USER_ID]
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
    cursor.close()

    return rDict
    # End of listUsers

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
