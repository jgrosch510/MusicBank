# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                         < common.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : common.py
#
# Author       : Josef Grosch
#
# Date         : 31 August 2021
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
#               (C) Copyright 2021 - 2023 Moose River LLC.
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

myhier = os.getenv('MYHIER')
gitHome = os.getenv('GIT_HOME')    
mbLibPath = os.getenv('MBLIBPATH')
sys.path.append(mbLibPath)

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

# --------------------------------------------------------------------
#
# 
#
# --------------------------------------------------------------------
"""

"""

    
# --------------------------------------------------------------------
#
# genReturnDict
#
# --------------------------------------------------------------------
def genReturnDict(msg = "") -> dict:
    """
    This sets up a dictonary that is intented to be returned from
    a function call. The real value here is that this dictonary
    contains information, like the function name and line number,
    about the function. This is handy when debugging a mis-behaving
    function.

    Args:
        msg: A text string containg a simple, short message

    Returns:
        r_dict: a dictonary that is returned from a function call

    """
    RS = ReturnStatus()

    r_dict = {}

    # These values come from the previous stack frame ie. the
    # calling function.
    r_dict['line_number']   = sys._getframe(1).f_lineno
    r_dict['filename']      = sys._getframe(1).f_code.co_filename
    r_dict['function_name'] = sys._getframe(1).f_code.co_name

    r_dict['status']   = RS.OK # See the class ReturnStatus
    r_dict['msg']      = msg   # The passed in string
    r_dict['data']     = ''    # The data/json returned from func call
    r_dict['path']     = ''    # FQPath to file created by func (optional)
    r_dict['resource'] = ''    # What resource is being used (optional)

    return r_dict
    # End of gen_return_dict


# --------------------------------------------------------------------
#
# class ReturnStatus
#
# --------------------------------------------------------------------
class ReturnStatus:
    """
    Since we can't have nice things, like #define, this is
    a stand in.

    These values are intended to be returned from a function
    call. For example

    def bar():
        RS = ReturnStatus()
        r_dict = genReturnDict('Demo program bar')

        i = 1 + 1

        if i == 2:
            r_dict['status'] = RS.OK
        else:
            r_dict['status'] = RS.NOT_OK
            r_dict['msg'] = 'Basic math is broken'

        return r_dict

    def foo():
        RS = ReturnStatus()

        r_dist = bar()
        if r_dict['status'] = RS.OK:
            print('All is right with the world')
        else:
            print('We're doomed!')
            print(r_dict['msg'])
            sys.exit(RS.NOT_OK)

        return RS.OK

    """
    
    OK         = 0 # It all worked out
    NOT_OK     = 1 # Not so much
    SKIP       = 2 # We are skipping this block/func
    NOT_YET    = 3 # This block/func is not ready
    FAIL       = 4 # It all went to hell in a handbasket
    NOT_FOUND  = 5 # Could not find what we were looking for
    FOUND      = 6 # Found my keys
    YES        = 7 # Cant believe I missed these
    NO         = 8 # Cant believe I missed these
    RESTRICTED = 9 #
    # End of class ReturnStatus

# --------------------------------------------------------------------
#
# class Tools
#
# --------------------------------------------------------------------
class Tools:
    """
    """
    Tools = [
        'add',     # MBAdd
        'backup',  # MBBackup
        'check',   # MBCheck
        'config',  # MBConfig
        'delete',  # MBDelete
        'fix',     # MBFix
        'help',    #
        'list',    # MBList
        'manage',  # MBManage
        'merge',   # MBMerge
        'move',    # MBMove
        'remove',  # MBRemove
        'rip',     # MBRip
        'update'   # MBUpdate
        ]
    
    # End of class Tools
    
# --------------------------------------------------------------------
#
# class UserTable
#
# --------------------------------------------------------------------
class UserTable:
    """
    """
    
    REC_NUM      = 0 #
    REC_VERSION  = 1 #
    INSERT_TIME  = 2 #
    INSERT_EPOCH = 3 #
    UPDATE_TIME  = 4 #
    UPDATE_EPOCH = 5 #
    ACTIVE       = 6 #
    USER_NAME    = 7 #
    USER_ID      = 8 #
    USER_EMAIL   = 9 #

    REC_NUM_MIN_WIDTH      =  7 #
    INSERT_TIME_MIN_WIDTH  = 15 #
    USER_NAME_MIN_WIDTH    = 15 #
    USER_ID_MIN_WIDTH      = 15 #
    USER_EMAIL_MIN_WIDTH   = 15 #

    # End of class UserTable

# --------------------------------------------------------------------
#
# class ArtistTable
#
# --------------------------------------------------------------------
class ArtistTable:
    """
    """
    
    REC_NUM      = 0 #
    # End of class ArtistTable

# --------------------------------------------------------------------
#
# class AlbumTable
#
# --------------------------------------------------------------------
class AlbunTable:
    """
    """
    
    REC_NUM      = 0 #
    # End of class AlbumTable

# --------------------------------------------------------------------
#
# class MusifFile
#
# --------------------------------------------------------------------
class MusicFile:
    """
    """
    MFILE = {
        "disk_ordnal": "",
        "track_ordnal": "",
        "file_name": "",
        "fqp": "",
        "set": "",
        "file_type": "",
        "title": "",
        "ffp": "",
        "sha256": "",
        "md5": ""
        }
    # End of class MusicFile

# --------------------------------------------------------------------
#
# class AlbumFile
#
# --------------------------------------------------------------------
class AlbumFile:
    """
    """
    ALBUM = {
        "title": "",
        "status": "",
        "barcode": "",
        "track_count": "",
        "disc_count": "",
        "collection_type": "",
        "artist": "",
        "url": "",
        "year": "",
        "date": "",
        "venue": "",
        "location": "",
        "genre": "",
        "sections": {
            "misc": "",
            "id_tags": {
                "asin": "",
                "etree_artist_key": "",
                "musicbrainz_artist_id": "",
                "musicbrainz_show_id": "",
                "musicbrainz_album_id": "",
                "shnid": "",
                "show_key": "",
                "torrent": ""
                }
            },
        "m3u": "",
        "admin": {
            "owner_id": "",
            "owner_email": ""
            },
        "images": [
            {
                "cover": {
                    "jpg": "",
                    "md5": "",
                    "sha512": ""
                    }
                }
            ],
        "tabs": {
            "bass": "",
            "guitar": ""
            },
        "music_files": []
            
        }

    # End of class AlbumFile
    """
    {
    "track_ordnal": "",
    "file": "",
    "set": "",
    "file_type": "",
    "disk_track": "",
    "title": "",
    "ffp": "",
    "sha256": "",
    "md5": ""
    }
    """            

# -----------------------------------------------------------------------
#
# End of common.py
#
# -----------------------------------------------------------------------
