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
#                   Copyright (c) 2020 - 2023 Moose River LLC.
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

#myhier = os.getenv('MYHIER')
#gitHome = os.getenv('GIT_HOME')    
mbLibPath = os.getenv('MBLIBPATH')
sys.path.append(mbLibPath)


import MBCommon as MBC
import MBDBUtil as MBDB

#--start constants--

__author__      = "Josef Grosch"
__copyright__   = "Copyright 2020 - 2023 Moose River, LLC."
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
                rDict['msg'] = f"{pDict['toolName']}: New user, {userId}, DB record inserted"
                         
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
    query = 'select * from user;'

    rDict = __listUsers(pDict, query)

    return rDict
    # End of listUsers

# ----------------------------------------------------------
#
# __listUsers
#
# ----------------------------------------------------------
def __listUsers(pDict, query):
    rDict = MBC.genReturnDict('inside __listUser')
    RS    = MBC.ReturnStatus
    UT    = MBC.UserTable
    
    JL = []
    UD = {}
    W = {}

    W['recNumWidth']     = 0
    W['userNameWidth']   = 0
    W['userIdWidth']     = 0
    W['userEmailWidth']  = 0
    W['insertTimeWidth'] = 0
    
    D = MBDB.connectToDB(pDict)
    cursor  = D['data']['cursor']
    conn    = D['data']['conn']
    
    cursor.execute(query)
    Rows = cursor.fetchall()
    if len(Rows) > 0:
        for row in Rows:
            UD['recNum'] = row[UT.REC_NUM]
            width = len(str(row[UT.REC_NUM]))
            if width > W['recNumWidth']:
                W['recNumWidth'] = width
                
            UD['recVersion']  = row[UT.REC_VERSION]
            
            UD['insertTime']  = row[UT.INSERT_TIME]
            width = len(row[UT.INSERT_TIME])
            if width > W['insertTimeWidth']:
                W['insertTimeWidth'] = width

            UD['insertEpoch'] = row[UT.INSERT_EPOCH]

            UD['updateTime']  = row[UT.UPDATE_TIME]

            UD['updateEpoch'] = row[UT.UPDATE_EPOCH]

            UD['active']      = row[UT.ACTIVE]

            UD['userName']    = row[UT.USER_NAME]
            width = len(row[UT.USER_NAME])
            if width > W['userNameWidth']:
                W['userNameWidth'] = width

            UD['userId']      = row[UT.USER_ID]
            width = len(row[UT.USER_ID])
            if width > W['userIdWidth']:
                W['userIdWidth'] = width

            UD['userEmail']   = row[UT.USER_EMAIL]
            width = len(row[UT.USER_EMAIL])
            if width > W['userEmailWidth']:
                W['userEmailWidth'] = width

            JL.append(UD)
            UD = {}
        # End of for loop

        pDict['W']  = W
        pDict['JL'] = JL
        outStr = genUserListingStr(pDict)
        
        rDict['status'] = RS.OK
        rDict['msg']    = f"{pDict['toolName']}: Users found"
        rDict['data']   = outStr
    else:
        rDict['status'] = RS.NOT_FOUND
        rDict['msg'] = f"{pDict['toolName']}: No users found"
    # End of if/else

    conn.commit()
    cursor.close()

    return rDict
    # End of __listUsers

# ----------------------------------------------------------
#
# genUserListingStr
#
# ----------------------------------------------------------
def genUserListingStr(pDict):
    rDict = MBC.genReturnDict('inside genUserListingStr')
    RS    = MBC.ReturnStatus
    UT    = MBC.UserTable

    JL = pDict['JL']
    W = pDict['W']
    
    outStr = ''
    Lines = []
    
    if W['recNumWidth'] < UT.REC_NUM_MIN_WIDTH:
        W['recNumWidth'] = UT.REC_NUM_MIN_WIDTH
                
    if W['userNameWidth'] < UT.USER_NAME_MIN_WIDTH:
        W['userNameWidth'] = UT.USER_NAME_MIN_WIDTH
            
    if W['userIdWidth'] < UT.USER_ID_MIN_WIDTH:
        W['userIdWidth'] = UT.USER_ID_MIN_WIDTH
            
    if W['userEmailWidth'] < UT.USER_EMAIL_MIN_WIDTH:
        W['userEmailWidth'] = UT.USER_EMAIL_MIN_WIDTH

    if W['insertTimeWidth'] < UT.INSERT_TIME_MIN_WIDTH:
        W['insertTimeWidth'] = UT.INSERT_TIME_MIN_WIDTH


    title1 = ' rec # '
    title1Len = len(title1)
    a = '-' * title1Len

    title2 = '   user name   '
    title2Len = len(title2)
    b = '-' * title2Len

    title3 = '    user id    '
    title3Len = len(title3)
    c = '-' * title3Len

    title4 = '           user email           '
    title4Len = len(title4)
    d = '-' * title4Len

    title5 = '            insert time           '
    title5Len = len(title5)
    e = '-' * title5Len

    headStr1 = f"+{a}+{b}+{c}+{d}+{e}+"
    headStr2 = f"|{title1}|{title2}|{title3}|{title4}|{title5}|"
    headStr = f"{headStr1}\n{headStr2}\n{headStr1}\n"
    Lines.append(headStr)
    #print(headStr)
    
    #'{:^10}'.format('test')
    for entry in JL:
        recNum     = str(entry['recNum'])
        userName   = entry['userName']
        userId     = entry['userId']
        userEmail  = entry['userEmail']
        insertTime = entry['insertTime']

        tmpStr = ("|{:^7}|{:^15}|{:^15}|{:^32}|{:^34}|\n"
                  .format(recNum, userName, userId, userEmail, insertTime))
        Lines.append(tmpStr)

    Lines.append(headStr1)
    outStr = ''.join(Lines)
    #print(outStr)
    
    return outStr
    # End of genUserListingStr
    
# ----------------------------------------------------------
#
# listUser
#
# ----------------------------------------------------------
def listUser(pDict):
    userId = pDict['id']
    query = f"select * from user where user_id = '{userId}';"

    rDict = __listUsers(pDict, query)

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


def getUserInfo(pDict):
    rDict = MBC.genReturnDict('inside updateUser')
    RS    = MBC.ReturnStatus

    UD = {}
    
    userId = pDict['id']
    query = f"select * from user where user_id = '{userId}';"

    D = MBDB.connectToDB(pDict)
    cursor  = D['data']['cursor']
    conn    = D['data']['conn']
    
    cursor.execute(query)
    Rows = cursor.fetchall()
    if len(Rows) == 1:
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
        # End of for loop
        
        rDict['status'] = RS.OK
        rDict['msg']    = 'User found'
        rDict['data']   = UD
    else:
        rDict['status'] = RS.NOT_FOUND
        rDict['msg'] = 'No user found'
    # End of if/else
    
    conn.commit()
    cursor.close()

    return rDict
    # End of updateUser
    
# -----------------------------------------------------------------------
#
# End of user.py
#
# -----------------------------------------------------------------------
