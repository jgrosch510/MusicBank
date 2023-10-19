#!/usr/bin/env python3
# -*- mode: python -*-
# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------
#
#                              < MBRip.py >
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
# File Name    : MBRip.py
#
# Author       : Josef Grosch
#
# Date         : 30 Aug 2023
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
#               Deadicated to my brother Jerry Garcia,
#            who passed from this life on August 9, 1995.
#                     Happy trails to you, Jerry
#
# -----------------------------------------------------------------------


# -----------------------------------------------------------------------
#
#                               GPG Key
#
# pub 4096R/C8FE7E3C 2019-05-07 [expires: 2021-05-06]
# Key fingerprint = E0BA 2A0F 0830 A58F 6319  FA19 1737 A401 C8FE 7E3C
# uid Josef Grosch <jgrosch@gmail.com>
# sub 4096R/1BD5EC2E 2019-05-07 [expires: 2021-05-06]
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

import os, sys

myhier = os.getenv('MYHIER')
gitHome = os.getenv('GIT_HOME')    
mbLibPath = os.getenv('MBLIBPATH')
sys.path.append(mbLibPath)

import argparse
import musicbrainzngs
import libdiscid
import json
import unidecode
import sqlite3

import configparser

from subprocess import Popen, PIPE
import subprocess
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
# main
#
# ----------------------------------------------------------
def main():
    RS = MBC.ReturnStatus
    D = {}    

    musicbrainzngs.set_useragent(
        "MMRip",
        "0.1",
        "https://github.com/jgrosch510/MBRip/tree/main"
        )

    params = loadConfigFile()

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-c", "--cdrom", help="provide the source of the cd",
                        default="/dev/cdrom")
    
    parser.add_argument("-d", "--debug", help="Debug option", action='store_true')

    parser.add_argument("-t", "--testing", help="Testing option", action='store_true')

    args = parser.parse_args()

    device  = args.cdrom
    debug   = args.debug
    testing = args.testing

    rDict = getDiscInfo(device)
    DiscInfo = rDict['data']
    discId = DiscInfo['id']
    if debug:
        jObj = json.dumps(rDict, indent=4)
        print(jObj)

    rDict = getArtistInfo(discId)
    ArtistInfo = rDict['data']
    if debug:
        jObj = json.dumps(rDict, indent=4)
        print(jObj)
        
    sys.exit(RS.OK)
    #
    # End of main
    #

def performAction(argv):
    print(str(argv))
    print(len(argv))

    return
    #

# ----------------------------------------------------------
#
# getArtistInfo
#
# ----------------------------------------------------------
def getArtistInfo(discId):
    RS = MBC.ReturnStatus
    rDict = MBC.genReturnDict('inside getArtistInfo')

    path = '/usr3/home/jgrosch/Git/MBRip'
    dbFile = f"{path}/Data/BandInfo.sqlite"

    BI = {}
    
    try:
        result = musicbrainzngs.get_releases_by_discid(discId, includes=["artists","recordings"])

        artistId = result['disc']['release-list'][0]['artist-credit'][0]['artist']['id']
        query = f"select * from band_info where music_brainz_index = '{artistId}';"

        conn = sqlite3.connect(dbFile)
        with conn:
            cur = conn.cursor()
            cur.execute(query)

            Rows = cur.fetchall()
            if len(Rows) == 1:
                for rows in Rows:
                    BI['rec_num']            = rows[0]
                    BI['dir']                = rows[1]
                    BI['music_bank_index']   = rows[4]
                    BI['music_brainz_index'] = rows[5]
                    BI['band_name']          = rows[6]
                    BI['dir_name']           = rows[7]
                
                    if rows[2] is None:
                        BI['etree_index'] = ''
                    else:
                        BI['etree_index'] = rows[2]

                    if rows[3] is None:
                        BI['band_url'] = ''
                    else:
                        BI['band_url'] = rows[3]
                # End of for loop
            # End of if

        BI['result'] = result
    except musicbrainzngs.ResponseError:
        rDict['msg'] = "Sorry, disc not found or bad response"
        rDict['status'] = RS.NOT_FOUND
    
    rDict['status'] = RS.OK
    rDict['data'] = BI
    
    return rDict
    # End of getArtistInfo
    
# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def loadConfigFile():
    RS = MBC.ReturnStatus
    rDict = MBC.genReturnDict('inside loadConfigFile')

    D = {}
    D['HOME'] = os.getenv('HOME')
    
    D['MUSIC_ROOT'] = os.getenv('MUSIC_ROOT')
    if not os.path.exists(D['MUSIC_ROOT']):
        os.makedirs(D['MUSIC_ROOT'])

    D['MUSIC_TMP'] = os.getenv('MUSIC_TMP')
    if D['MUSIC_TMP'] is not None:
        if not os.path.exists(D['MUSIC_TMP']):
            os.makedirs(D['MUSIC_TMP'])

    D['BAND_INFO_FILE'] = f"{D['HOME']}/.mbrip/BandInfo.json"
    with open(D['BAND_INFO_FILE'], 'r') as fh:
        Lines = fh.read()

    bandInfo = json.loads(Lines)
    D['BAND_INFO'] = bandInfo
    
    config = configparser.ConfigParser()
    #if not os.path.exists('
    #configFile
    #config.read('example.ini')

    return rDict
    # End of

# ----------------------------------------------------------
#
# getDiscInfo
#
# ----------------------------------------------------------
def getDiscInfo(device='/dev/cdrom'):
    RS = MBC.ReturnStatus
    rDict = MBC.genReturnDict('inside getDiscInfo')

    DiscInfo = {}

    disc = libdiscid.read(device)

    DiscInfo['device']         = disc.device
    DiscInfo['first_track']    = disc.first_track
    DiscInfo['freedb_id']      = disc.freedb_id
    DiscInfo['id']             = disc.id
    DiscInfo['last_track']     = disc.last_track
    DiscInfo['leadout_track']  = disc.leadout_track
    DiscInfo['mcn']            = disc.mcn
    DiscInfo['pregap']         = disc.pregap
    DiscInfo['sectors']        = disc.sectors
    DiscInfo['submission_url'] = disc.submission_url 
    DiscInfo['toc']            = disc.toc
    DiscInfo['track_isrcs']    = disc.track_isrcs
    DiscInfo['track_lengths']  = disc.track_lengths
    DiscInfo['track_offsets']  = disc.track_offsets
    DiscInfo['webservice_url'] = disc.webservice_url

    rDict['status'] = RS.OK
    rDict['data'] = DiscInfo
    
    return rDict
    # ENd of getDiscInfo
    
# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def addStatus():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def cddbSum():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def checkErrors():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def checkExec():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def checkStatus():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def checkWarnings():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def decho():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def diffentries():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doBatchGain():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doBatchNormalize():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doCddbRead():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doCddbEdit():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doCddbParse():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doCdRead():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doCdSpeed():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doCdTextRead():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doCleanCu():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doDiscId():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doEmbedAlbumar():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doEncode():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doGetAlbumar():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doGetGenreId():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doLocalCddbRead():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doMove():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doMusicBrainzRead():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doNoGapEncode():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doNormalize():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doPlaylist():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doPostProcess():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doPreProcess():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doReplayGai():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doSingleGain():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def doTag():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def echoMsf():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def fseqline():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def fseqrow():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def getFirs():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def getLas():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def getCddbInf():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def getTrackNumber():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def log():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def makeIds():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def msf2lba():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def mungeAlbumName():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def mungeArtistName():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def mungeFileName():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def mungeGenre():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def mungeTrackName():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def newCheckexec():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def page():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def postEncode():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def postRead():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def preRead():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def relPath():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def runCommand():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def slash():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def splitVarious():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def usage():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def vecho():
    pass
    # End of

# ----------------------------------------------------------
#
#
#
# ----------------------------------------------------------
def vvecho():
    pass
    # End of


# ----------------------------------------------------------
#
# Entry point
#
# ----------------------------------------------------------
if __name__ == '__main__':
    main()
    

# -----------------------------------------------------------------------
#
# End of MBRip.py
#
# -----------------------------------------------------------------------
