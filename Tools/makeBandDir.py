#!/usr/bin/env python3
# -*- mode: python -*-
# -*- coding: utf-8 -*-


import os, sys
import json
import argparse
from subprocess import Popen, PIPE
import subprocess
from MusicBank import MB_common as MBC


# --------------------------------------------------------------------
#
# main
#
# --------------------------------------------------------------------
def main():
    testing = False
    RS = MBC.ReturnStatus

    musicHome = os.getenv('MUSIC_ROOT')
    if musicHome is None:
        print("\nERROR: Environment variable, MUSIC_ROOT, is not set.\nTry again.")
        sys.exit(RS.NOT_OK)

    if not os.path.exists(musicHome):
        print(f"ERROR: The directory, {musicHome} not found.\n")
        print("Run the script mkMusicBankTree.sh to create the basic dir tree.")
        sys.exit(RS.NOT_OK)

    parser = argparse.ArgumentParser()

    parser.add_argument("--band", help='Band to search for', required=True)

    args = parser.parse_args()

    bandName = args.band
    D = bandSearch(bandName)
    if D['status'] == RS.NOT_OK:
        print(D['msg'])
    else:
        bandName = D['data']['name']
        bandDir  = D['data']['dir']
                
        bandHome  = f"{musicHome}/Alpha/{bandDir}/{bandName}"
        bandHome2 = f"{bandHome}/Live-Recordings"
        bandHome3 = f"{bandHome}/Misc"
        bandHome4 = f"{bandHome}/Notes"
        bandHome5 = f"{bandHome}/PlayLists"
        cmdList = [bandHome2, bandHome3, bandHome4, bandHome5]

        for cmd in cmdList:
            result = subprocess.run(
                ["mkdir", "-p", cmd],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
                )

            sOut = result.stdout
        # End of for loop
    # End of if/else

    print(f"The home dir for {bandName} has been created at {bandHome}")
    sys.exit(RS.OK)
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

# --------------------------------------------------------------------
#
# entry point
#
# --------------------------------------------------------------------
if __name__ == '__main__':
    main()


