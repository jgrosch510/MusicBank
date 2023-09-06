#!/usr/bin/env python3
# -*- mode: python -*-
# -*- coding: utf-8 -*-

import os
import sys
import argparse
import musicbrainzngs
import libdiscid
import json
import unidecode
from subprocess import Popen, PIPE
import subprocess
from MusicBank import MB_common as MBC

 
# ----------------------------------------------------------
#
# main
#
# ----------------------------------------------------------
def main():
    RS = MBC.ReturnStatus
    D = {}

    rDict = loadConfigFile()
    D = rDict['data']
    
    musicbrainzngs.set_useragent("MusicBank", "0.1", "https://github.com/jgrosch510/MusicBank")

    parser = argparse.ArgumentParser()
    
    parser.add_argument("-c", "--cdrom", help="provide the source of the cd",
                        default="/dev/cdrom")
    
    parser.add_argument("-d", "--debug", help="Debug option", action='store_true')

    parser.add_argument("-t", "--testing", help="Testing option", action='store_true')

    args = parser.parse_args()

    device  = args.cdrom
    debug   = args.debug
    testing = args.testing

    if testing:
        D['MUSIC_ROOT'] = f"{D['HOME']}/MooseRiver/MusicBank"

    if debug:
        print('-'*40)
        print(f"device: {device}")

    print("Getting the disc ID, this can take up to 2 minutes.")
    disc = libdiscid.read(device)
    i = 0

    if debug:
        print(f"id: {disc.id}")
        print('-'*40)

    try:
        result = musicbrainzngs.get_releases_by_discid(disc.id, includes=["artists","recordings"])
        D['result'] = result
        
        if debug:
            print('-'*40)
            jObj = json.dumps(result, indent=4)
            print(jObj)
        
        artist = result['disc']['release-list'][0]['artist-credit'][0]['artist']['name']
        rDict = bandSearch(artist)
        artist = rDict['data']['name']
        artistDir = rDict['data']['dir']
        artistPath = f"{D['MUSIC_ROOT']}/Alpha/{artistDir}/{artist}"
        
        albumTitle = result['disc']['release-list'][0]['title']
        albumTitle = albumTitle.replace(' ', '-').replace(',', '').replace('.', '')
        albumPath = f"{artistPath}/{albumTitle}"
        if not os.path.exists(albumPath):
            os.makedirs(albumPath)

        albumJson = f"{albumTitle}.MusicBranz-Dump.json"
        jsonFile = f"{albumPath}/{albumJson}"
        resultJson = json.dumps(result, indent=4, ensure_ascii=True)
        with open(jsonFile, 'w') as fp:
            fp.write(resultJson)
            fp.close()
        
        trackList = result['disc']['release-list'][0]['medium-list'][0]['track-list']
        musicbranz_id = disc.id
        freedb_id = disc.freedb_id

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
        print("disc not found or bad response")
    else:
        if debug:
            print('-'*40)

    sys.exit(RS.OK)
    #
    # End of main
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
    #
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

# ----------------------------------------------------------
#
# Entry point
#
# ----------------------------------------------------------
if __name__ == '__main__':
    main()
