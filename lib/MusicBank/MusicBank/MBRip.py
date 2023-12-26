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

import audio_metadata
import hashlib
import json
import libdiscid
import magic
import musicbrainzngs
import sqlite3
import unicodedata
import unidecode

from subprocess import Popen, PIPE
import subprocess

import MBCommon as MBC
import MBUser as MBU
import MBConfig


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

"""

 # ----------------------------------------------------------
#
# performAction
#
# ----------------------------------------------------------
def performAction(pDict):
    rDict = MBC.genReturnDict('inside MBAdd.performAction')
    RS    = MBC.ReturnStatus

    argv     = pDict['argv']
    argc     = pDict['argc']
    config   = pDict['config']
    action   = pDict['action']
    argsList = pDict['argsList']
        
    helpFound = False
    cmdDone = False
    debug = False
    if debug:
        print(str(argv))
        print(len(argv))

    pDict['cdrom'] = '/dev/cdrom'
    
    for entry in argsList:
        index = entry['index']
        key   = entry['key']
        value = entry['value']

        if 'calling program' in value:
            continue

        if 'cmd' in value:
            continue

        if 'skip' in value:
            continue

        if '--cdrom' in key:
            pDict['cdrom'] = value
            continue
            
        if '--offical' in key:
            pDict['offical'] = value
            continue
            
        if '--id' in key:
            pDict['id'] = value
            continue

        if '--help' in key:
            msg = returnMasterHelp()
            helpFound = True
            break
    i = 0
    
    if helpFound == False:
        # CDROM
        if 'cdrom' in pDict and not cmdDone:
            i = 1
            tmpDict = myMain(pDict)
            cmdDone = True

        # Id
        """
        if 'id' in pDict and not cmdDone:
            i = 4
            tmpDict = MBU.addUser(pDict)
            cmdDone = True
        """
        
        rDict['status'] = tmpDict['status']
        rDict['msg'] = tmpDict['msg']
    else:
        # --help found. Return help
        rDict['msg'] = msg
        rDict['status'] = RS.OK
    
    return rDict
    
    # End of performAction

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
# loadConfigFile
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
    # End of loadConfigFile

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
# myMain
#
# ----------------------------------------------------------
def myMain(pDict):
    RS = MBC.ReturnStatus
    D = {}
    primaryD = {}
    
    cDict            = {}
    cDict['HOME']    = os.getenv('HOME')
    cDict['myhier']  = os.getenv('MYHIER')
    cDict['gitHome'] = os.getenv('GIT_HOME')    

    A2 = MBC.AlbumFile()
    A = A2.ALBUM
    
    musicbrainzngs.set_useragent("MusicBank",
                                 "0.1",
                                 "https://github.com/jgrosch510/MusicBank")
    device  = pDict['cdrom']
    debug   = False
    testing = False
        
    rDict = MBConfig.performAction(cDict)
    D = cDict['env']

    print("Getting the disc ID, this can take up to 2 minutes.")
    #device = pDict['cdrom']
    disc = libdiscid.read(device)
    rDict = captureDiscInfo(disc)
    primaryD['disc'] = rDict['data']
    
    if debug:
        print(f"id: {disc.id}")
        print('-'*40)

    try:
        result = musicbrainzngs.get_releases_by_discid(disc.id, includes=["artists","recordings"])
        if not None in result:
            primaryD['musicbranzResult'] = result['disc']

        ReleaseList = result['disc']['release-list']
        selectedIndex = 0

        if result['disc']['release-count'] > 1:
            entryCount = result['disc']['release-count']
            Barcodes = []
            ReleaseList = result['disc']['release-list']
            rDict = genSelectionText(ReleaseList)

            print("\nMultiple release entries found.\n")
            print("Select the entry you have.\n")
            print(rDict['msg'])

            looking = True
            while looking:
                data = input(f"Please an entry (1 - {entryCount}): ")
                dataInt = int(data)
                if (dataInt >= 1) and (dataInt <= entryCount):
                    selectedEntry = dataInt
                    looking = False
            selectedIndex = (dataInt - 1)
        
        selectedResult = ReleaseList[selectedIndex]
        result['disc']['selected-release'] = selectedResult
            
        if debug:
            print('-'*40)
            jObj = json.dumps(result, indent=4)
            print(jObj)
        
        artist = result['disc']['release-list'][0]['artist-credit'][0]['artist']['name']
        rDict = bandSearch(artist)
        artist = rDict['data']['name']
        artistDir = rDict['data']['dir']
        artistPath = f"{D['MUSIC_ROOT']}/{D['MB_USER_ID']}/Alpha/{artistDir}/{artist}"
        
        albumTitle = result['disc']['release-list'][0]['title']
        albumTitleOrig = albumTitle
        albumTitle = albumTitle.replace('&', 'And')
        albumTitle = albumTitle.replace(' ', '-').replace(',', '').replace('.', '')
        albumPath = f"{artistPath}/{albumTitle}"
        if not os.path.exists(albumPath):
            os.makedirs(albumPath)

        albumJson = f"{albumTitle}.MusicBranz-Dump.json"
        jsonFile = f"{albumPath}/{albumJson}"
        resultJson = json.dumps(result, indent=4, ensure_ascii=True)
        with open(jsonFile, 'w') as fp:
            fp.write(resultJson)

        print(f"Wote album json to {jsonFile}")

        pDict = {}
        pDict['cDict']  = cDict
        pDict['inFile'] = jsonFile
        pDict['basePath'] = albumPath

        # Album json
        rDict = fixFileNames(pDict)
        pDict['correctedNames'] = rDict['data']
        rDict = genAlbumDict(pDict)
        album = rDict['data']
        outJson = json.dumps(album, indent=4)
        
        debug = False
        if debug:
            print(outJson)

        albumJsonFile = f"{pDict['basePath']}/album.json"
        with open(albumJsonFile, 'w') as fh:
            fh.write(outJson)

        # FFP File
        ffp = 0
        pDict['album'] = album
        pDict['albumTitle'] = albumTitle
        rDist = genFfpFile(pDict)
        
        trackList = result['disc']['release-list'][0]['medium-list'][0]['track-list']
        musicbranz_id = disc.id
        freedb_id = disc.freedb_id

        D['result'] = result
        # Fill out Album
        disc = result['disc']
        A['artist'] = artist
        A['title'] = albumTitleOrig
        A['status'] = disc['selected-release']['status']
        A['collection_type'] = 'album'

        if debug:
            print('-'*40)
            tList = json.dumps(trackList, indent=4)
            print(tList)
            print('-'*40)
            
            listLen = len(trackList)

            for index in range(0, listLen):
                entry = trackList[index]
                tmpTitle = entry['recording']['title']
                title2 = unidecode.unidecode(tmpTitle)
                print("Title : {}".format(title2))
        # End if debug
        
    except musicbrainzngs.ResponseError:
        print("Sorry, disc not found or bad response.\n")
        subURL = disc.submission_url
        print(subURL)
        print('\n')
        sys.exit(RS.NOT_FOUND)
    else:
        if debug:
            print('-'*40)

    return
    #
    # End of myMain
    #

# ----------------------------------------------------------
#
# loadConfigFile
#
# ----------------------------------------------------------
def loadConfigFile():
    RS = MBC.ReturnStatus
    rDict = MBC.genReturnDict('inside loadConfigFile')

    D = {}
    
    home = os.environ['HOME']
    D['HOME'] = home
    configFile = "/usr/local/site/etc/MusicBankConfig.json"

    if not os.path.exists(configFile):
        rDict['status'] = RS.NOT_FOUND
        rDict['msg'] = f"ERROR: {configFile} NOT found."
    else:
        with open(configFile, "r") as read_file:
            data = json.load(read_file)

        D['OWNER_EMAIL']      = data['owner_email']
        D['OWNER_GPG_KEY_ID'] = data['owner_gpg_key_id']
        D['MUSIC_ROOT']       = data['music_root']

        if not os.path.exists(D['MUSIC_ROOT']):
            os.makedirs(D['MUSIC_ROOT'])
            
        rDict['status'] = RS.OK
        rDict['data'] = D
        
    return rDict 
    #
    # End of loadConfigFile
    #

# ----------------------------------------------------------
#
# genLocationStr
#
# ----------------------------------------------------------
def genLocationStr(D):
    result= D['result']
    startChar = ''
    
    artist = result['disc']['release-list'][0]['artist-credit'][0]['artist']['name']
    artistType = result['disc']['release-list'][0]['artist-credit'][0]['artist']['type']
    sortName = result['disc']['release-list'][0]['artist-credit'][0]['artist']['sort-name']

    if artistType == 'Person':
        startChar = sortName[0]
        artist = artist.replace(' ', '-')
    else:
        artistBits = artist.split()
        artistBitsLen = len(artistBits)
        artist = artist.replace(' ', '-')
        startChar = artist[0]

    albumTitle = result['disc']['release-list'][0]['title']
    titleBits = albumTitle.split()
    albumTitle = albumTitle.replace(' ', '-')

    musicRoot = D['MUSIC_ROOT']
    locationStr = f"{musicRoot}/Alpha/{startChar}/{artist}/{albumTitle}"
    
    return locationStr
    #
    # End of genLocationStr
    #

# --------------------------------------------------------------------
#
# bandSearch
#
# --------------------------------------------------------------------
def bandSearch(bandName: str) -> dict:
    rDict = MBC.genReturnDict('inside connectToDatabaseJson')
    RS    = MBC.ReturnStatus

    bandFound = False
    inFile = '/usr/local/site/data/BandDirs.json'
    
    if ' ' in bandName:
        bandName = bandName.replace(' ', '-')
            
    with open(inFile, 'r') as fh:
        Lines = fh.read()

    jObj = json.loads(Lines)
    for entry in jObj:
        Dir = entry['dir'].upper()
        Name = entry['name']
        if Name.lower() == bandName.lower():
            rDict['msg'] = f"Band found: {Name}"
            rDict['status'] = RS.OK
            rDict['data'] = entry
            bandFound = True
            break
            
    if not bandFound:
        tmpStr = f"\nThe band, {bandName}, not found.\n"
        tmpStr += "Are you sure you spelled it right?\n"
        tmpStr += f"If yes please update {inFile}\n"
        rDict['status'] = RS.NOT_OK
        rDict['msg'] = tmpStr

    return rDict
    # End of bandSearch

# ----------------------------------------------------------
#
# captureDiscInfo
#
# ----------------------------------------------------------
def captureDiscInfo(disc):
    RS = MBC.ReturnStatus
    rDict = MBC.genReturnDict('inside captureDiscInfo')

    D = {}

    D['device']         = disc.device
    D['first_track']    = disc.first_track
    D['freedb_id']      = disc.freedb_id
    D['id']             = disc.id
    D['last_track']     = disc.last_track
    D['leadout_track']  = disc.leadout_track
    D['mcn']            = disc.mcn
    D['pregap']         = disc.pregap
    D['sectors']        = disc.sectors
    D['submission_url'] = disc.submission_url
    D['toc']            = disc.toc
    D['track_isrcs']    = disc.track_isrcs
    D['track_lengths']  = disc.track_lengths
    D['track_offsets']  = disc.track_offsets
    D['webservice_url'] = disc.webservice_url

    rDict['status'] = RS.OK
    rDict['msg']    = 'Disc data loaded'
    rDict['data']   = D
          
    return rDict
    #
    # End of captureDiscInfo
    #

# ----------------------------------------------------------
#
# genSelectionText
#
# ----------------------------------------------------------
def genSelectionText(ReleaseList):
    RS = MBC.ReturnStatus
    rDict = MBC.genReturnDict('inside genSelectionText')
    
    infoList = []
    D = {}

    debug = False
        
    for entry in ReleaseList:
        if 'barcode' in entry:
            D['barcode'] = entry['barcode']
        else:
            D['barcode'] = ''

        if 'date' in entry:
            D['date'] = entry['date']
        else:
            D['date'] = ''
            
        if 'country' in entry:
            D['country'] = entry['country']
        else:
            D['country'] = ''
                
        if 'disambiguation' in entry:
            D['notes'] = entry['disambiguation']
        else:
            D['notes'] = ''

        if 'title' in entry:
            D['title'] = entry['title']
        else:
            D['title'] = ''
                
        infoList.append(D)
        D = {}
    # End of for loop
    
    aList = []
    index = 1
    for entry in infoList:
        barcode = entry['barcode']
        country = entry['country']
        date    = entry['date']
        tmpStr = '# {} - barcode: {:>14} country: {:>4} date: {:>10}\n'.format(index, barcode, country, date)
        
        aList.append(tmpStr)
        index += 1

    outStr = "".join(aList)
    rDict['status'] = RS.OK
    rDict['msg'] = outStr
    
    return rDict
    #

# ----------------------------------------------------------
#
# genAlbumDict
#
# ----------------------------------------------------------
def genAlbumDict(pDict):
    RS = MBC.ReturnStatus()
    rDict = MBC.genReturnDict('Insid genAlbumDict')
    
    debug = False
    T2 = MBC.Tools()
    Tools = T2.Tools
    ToolsTest = MBC.Tools().Tools

    cDict = pDict['cDict']
    env = cDict['env']
    musicRoot = env['MUSIC_ROOT']
    basePath = pDict['basePath']
    inFile = pDict['inFile']

    with open(inFile, 'r') as fh:
        xLines = fh.read()

    D = json.loads(xLines)

    A2 = MBC.AlbumFile()
    A = A2.ALBUM
        
    mList = []

    disc = D['disc']
    SR = disc['selected-release']
    TL = SR['medium-list'][0]['track-list']

    A['admin']['owner_id'] = cDict['config']['user']['mb_user_id']
    A['admin']['owner_email'] = cDict['config']['user']['mb_user_email']
    A['artist'] = SR['artist-credit'][0]['artist']['name']
    A['title'] = SR['title']
    A['status'] = SR['status']
    
    if 'barcode' in SR:
        A['barcode'] = SR['barcode']
        
    A['collection_type'] = 'album'
    A['sections']['id_tags']['musicbrainz_album_id'] = disc['id']
    
    if 'asin' in SR:
        A['sections']['id_tags']['asin'] = SR['asin']

    A['disc_count'] = '1'
    A['track_count'] = len(TL)
    A['date'] = SR['date']
    bits = SR['date'].split('-')
    A['year'] = bits[0]
    A['sections']['id_tags']['musicbrainz_artist_id'] = SR['artist-credit'][0]['artist']['id']

    MF = {}
    for entry in TL:
        MF['disk_ordnal'] = "1"
        MF['track_ordnal'] = entry['number']
        MF['title'] = entry['recording']['title']
        MF['file_name'] = ''
        MF['fqp'] = ''
        MF['set'] = '0'
        MF['file_type'] = ''
        MF['ffp'] = ''
        MF['sha256'] = ''
        MF['md5'] = ''

        mList.append(MF)
        MF = {}
    # End of for loop

    fileFound = False
    diskPath = f"{basePath}/Disc-01"
    flacList = []
    for root,d_names,f_names in os.walk(diskPath):
        r = root
        Dirs = d_names
        Files = f_names

        if len(Files) > 0:
            for entry in Files:
                if entry.endswith('.flac'):
                    fileFound = False
                    flacList.append(f"{root}/{entry}")
                    """
                    cleanName = entry.lower()
                    if cleanName[0].isdigit() and cleanName[1].isdigit():
                        cleanName = cleanName[4:]
                    cleanName = cleanName.replace('-', ' ')
                    cleanName = cleanName.replace('_', ' ')
                    cleanName = cleanName.replace('.flac', '')
                    """
                    cleanName = cleanFileName(entry)
                    for entry2 in mList:
                        title = entry2['title'].lower()
                        if title == cleanName:
                            j = 0
                            fileFound = True
                            entry2['file_name'] = entry
                            fqp = f"{diskPath}/{entry}"
                            entry2['fqp'] = fqp
                            entry2['file_type'] = magic.from_file(fqp)
                            m = audio_metadata.load(fqp)
                            ffp = m['streaminfo']['md5']
                            entry2['ffp'] = ffp
                            
                            with open(fqp,"rb") as f:
                                bytes = f.read() # read file as bytes
                                hashMd5 = hashlib.md5(bytes).hexdigest();
                                hashSha256 = hashlib.sha256(bytes).hexdigest();
                                entry2['md5'] = hashMd5
                                entry2['sha256'] = hashSha256
                        else:
                            j = 1
                            fileFound = False
                        # End of if/else
                    # End of for loop
                # End of if
            # End of for loop
        # End of if
    # End of for loop
                    
    A['music_files'] = mList
    rDict['data'] = A
    
    return rDict
    #
    
# --------------------------------------------------------------------
#
# genFfpFile
#
# --------------------------------------------------------------------
def genFfpFile(pDict):
    RS = MBC.ReturnStatus
    rDict = MBC.genReturnDict('inside genFfFile')

    ffpFile = f"{pDict['basePath']}/{pDict['albumTitle']}.ffp"
    fh = open(ffpFile, 'w')
    
    musicFiles = pDict['album']['music_files']
    for entry in musicFiles:
        fileName = entry['file_name']
        ffp = entry['ffp']
        ffpStr = f"{fileName}:{ffp}\n"
        fh.write(ffpStr)
        
    fh.close()
    
    return rDict

# ----------------------------------------------------------
#
# cleanFileName
#
# ----------------------------------------------------------
def cleanFileName(fName):
    cn = fName.lower()

    if cn[0].isdigit() and cn[1].isdigit():
        cn = cn[4:]
        
    #>>> unicodedata.normalize('NFKD', title).encode('ascii','ignore')
    test1 = unicodedata.normalize('NFKD', cn).encode('ascii','ignore')
    test2 = test1.decode('ascii')
    
    #cn = cn.decode('utf-8')
    #bs = bytes(cn, 'utf-8')
    #cn = bs.decode('ascii')

    cn = test2
    cn = cn.replace('-', ' ')
    cn = cn.replace('_', ' ')
    cn = cn.replace('.flac', '')
    cn = cn.replace('\'', '')
    cn = cn.replace('\`', '')
    cn = cn.replace("'", '')
    cn = cn.replace('(', '')
    cn = cn.replace(')', '')
    cn = cn.replace('&', 'And') 

    return cn
    # End of cleanFileName

# -----------------------------------------------------------------------
#
# toAsciiFileName
#
# -----------------------------------------------------------------------
def toAsciiFileName(fName):
    cn = fName

    if cn[0].isdigit() and cn[1].isdigit():
        a = cn[4:]
        prefix = cn[:4]
        
    test1 = unicodedata.normalize('NFKD', cn).encode('ascii','ignore')
    cn = test1.decode('ascii')

    cn = cn.replace('_', '-')
    cn = cn.replace('\'', '')
    cn = cn.replace('\`', '')
    cn = cn.replace("'", '')
    cn = cn.replace('(', '')
    cn = cn.replace(')', '')
    cn = cn.replace('&', 'And') 

    return cn

# -----------------------------------------------------------------------
#
# fixFileNames
#
# -----------------------------------------------------------------------
def fixFileNames(pDict):
    RS = MBC.ReturnStatus
    rDict = MBC.genReturnDict('inside genFfFile')

    basePath = pDict['basePath']
    diskPath = f"{basePath}"

    TrackList = []
    for root,d_names,f_names in os.walk(diskPath):
        r = root
        Dirs = d_names
        Files = f_names

        if 'Save' in root:
            continue

        if len(Files) > 0:
            for entry in Files:
                if entry.endswith('.flac'):
                    D = {}
                    entry2 = toAsciiFileName(entry)
                    origFileName = f"{root}/{entry}"
                    cleanedFileName = f"{root}/{entry}"
                    if entry[0].isdigit() and entry[1].isdigit():
                        prefix = entry[:2]
                        if prefix.startswith('0'):
                            prefix = prefix[1:2]

                    D['path']          = root
                    D['trackNumber']   = prefix
                    D['origFileName']  = entry
                    D['fixedFileName'] = entry2

                    TrackList.append(D)
                    D = {}
                # End of if
            # End of for
        # End of if

    for entry in TrackList:
        path          = entry['path']
        origFileName  = entry['origFileName']
        fixedFileName = entry['fixedFileName']

        sourceName = f"{path}/{origFileName}"
        destName   = f"{path}/{fixedFileName}"
        os.rename(sourceName, destName)
        
    rDict['status'] = RS.OK
    rDict['msg']    = 'Fixed'
    rDict['data']   = TrackList
    
    return rDict

# -----------------------------------------------------------------------
#
# End of MBRip.py
#
# -----------------------------------------------------------------------
