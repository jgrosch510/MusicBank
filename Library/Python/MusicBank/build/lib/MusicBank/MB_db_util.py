# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                            < MB_db_util.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : MB_db_util.py
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
import MB_common
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
def connectToDatabaseJson(param_file):
    """
    Abstracts making a connection to a database
    """

    rDict = genReturnDict('inside connectToDatabaseJson')
    RS    = ReturnStatus
    
    dbh = ""
    D = {}
    conn = ""
    cursor = ""
    
    data = __getDbParams(param_file)
    if data['loaded']:
        dbName   = data['db_name']
        dbHost   = data['hostname']
        dbUser   = data['user']
        dbPasswd = data['password']

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
    
    return D
    #
    # End of conectToDatabaseJson
    #

    
# ---------------------------------------------------------
#
# __getDbParams
#
# ---------------------------------------------------------
def __getDbParams(paramFile):
    """
    Internal function to read the database connection config file
    """
    data = {}
    data['loaded'] = False

    if os.path.exists(param_file) and os.path.isfile(param_file):
        with open(paramFile, 'r') as fh:
            Lines = fh.read()

        jObj = json.loads(Lines)
        
        data['db_name']  = jObj['db_name'] 
        data['hostname'] = jObj['hostname'] 
        data['password'] = jObj['password'] 
        data['user']     = jObj['user'] 

        data['loaded'] = True
    else:
        data['loaded'] = False
             
    return data
    #
    # End of __getDbParams
    #


# -----------------------------------------------------------------------
#
# End of MR_db_util.py
#
# -----------------------------------------------------------------------
