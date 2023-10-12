# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                            < db_util.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : db_util.py
#
# Author       : Josef Grosch
#
# Date         : 25 May 2015
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
#               (C) Copyright 2015 - 2023 Moose River LLC.
#                      <jgrosch@mooseriver.com>
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
# pub   rsa4096 2022-01-22 [SC] [expires: 2024-01-22]
# Key   fingerprint = D36 0ABF 3C34 858F 617F C6C8 887F E74C D0D5 6DFE2
# uid   [ultimate] Josef Grosch <jgrosch@gmail.com>
# sub   rsa4096 2022-01-22 [E] [expires: 2024-01-22]
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
import mysql.connector
import sqlite3
from MusicBank import MB_common as MBC
from mysql.connector import errorcode

try:
    import warnings
except ImportError:
    warnings = None


# --------------------------------------------------------------------
#
# 
#
# --------------------------------------------------------------------
"""
MR.db_util - Provides database access routines
"""

__revision__   = "0.2"
__author__     = "Josef Grosch"
__copyright__  = "Copyright 2015 - 2023 Moose River, LLC."
__license__    = "BSD-2-Clause"
__version__    = "0.2"
__maintainer__ = "Josef Grosch"
__email__      = "jgrosch@gmail.com"
__status__     = "Development"


# ---------------------------------------------------------
#
# connectToDatabaseJson
#
# ---------------------------------------------------------
def connectToDatabaseJson(paramFile: str) -> dict:
    """
    Abstracts making a connection to a database
    """

    rDict = MBC.genReturnDict('inside connectToDatabaseJson')
    RS    = MBC.ReturnStatus
    
    dbConnect = {}
    conn = ""
    cursor = ""

    if os.path.exists(paramFile) and os.path.isfile(paramFile):
        with open(paramFile, 'r') as fh:
            Lines = fh.read()

        jObj = json.loads(Lines)
        
        dbName   = jObj['db_name'] 
        dbHost   = jObj['hostname'] 
        dbPasswd = jObj['password'] 
        dbUser   = jObj['user'] 

        try:
            conn = mysql.connector.connect(user=dbUser,
                                           password=dbPasswd,
                                           host=dbHost,
                                           database=dbName)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        cursor = conn.cursor(buffered=True)
        
    dbConnect['conn']   = conn
    dbConnect['cursor'] = cursor

    rDict['status'] = RS.OK
    rDict['data']   = dbConnect
    
    
    return rDict
    #
    # End of conectToDatabaseJson
    #


# ----------------------------------------------------------
#
# connectToDB
#
# ----------------------------------------------------------
def connectToDB(pDict):
    rDict = MBC.genReturnDict('inside connectToDB')
    RS    = MBC.ReturnStatus

    D = {}
    Config = pDict['config']
    dbType = Config['db']['mb_db_type']

    if 'sqlite' in dbType:
        # sqlite3
        dbFile = f"{pDict['musicRoot']}/etc/MusicBank.sqlite"
        if not os.path.exists(dbFile):
            rDict['status'] = RS.NOT_FOUND
            rDict['msg'] = f"ERROR: {dbFile} NOT found."
        else:
            conn = sqlite3.connect(dbFile)
            cursor = conn.cursor()
            D['conn'] = conn
            D['cursor'] = cursor
            
            rDict['status'] = RS.OK
            rDict['msg'] = 'Connection made'
            rDict['data'] = D
    elif ('mysql' in dbType) or ('mariadb' in dbType):
        # MYSQL
        dbName   = Config['db']['mb_db_name'] 
        dbHost   = Config['db']['mb_db_host'] 
        dbPasswd = Config['db']['mb_db_password'] 
        dbUser   = Config['db']['mb_db_user'] 

        try:
            conn = mysql.connector.connect(user=dbUser,
                                           password=dbPasswd,
                                           host=dbHost,
                                           database=dbName)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

        cursor = conn.cursor(buffered=True)
        
    D['conn']   = conn
    D['cursor'] = cursor

    rDict['status'] = RS.OK
    rDict['data']   = D
        
    return rDict
    # End of connectToDB

# -----------------------------------------------------------------------
#
# End of db_util.py
#
# -----------------------------------------------------------------------
