#!/usr/bin/env python3
# -*- mode: python -*-
# -*- coding: utf-8 -*-

import os
import sys
import json
import sqlite3
import uuid
import argparse

from MooseRiver import MR_string_util as MRSU

def main():
    D       = {}
    index   = 0
    homeDir = os.getenv('HOME')
    base    = f"{homeDir}/GitHub/MusicBank/Data/Grateful-Dead"
    dbFile  = f"{base}/GD-Shows-TEST.sqlite"
    outFile = ''

    parser = argparse.ArgumentParser()

    parser.add_argument("--all", help='All years', action='store_true')

    parser.add_argument("--insert", help='Insert query', action='store_true')

    parser.add_argument("--output", help='write out insert statements',
                        action='store_true')

    parser.add_argument("--quiet", help='No stdout output', action='store_true')

    parser.add_argument("--year", help='Year to process', required=True)

    args = parser.parse_args()

    year = args.year
    yearInt = int(year)
    
    if yearInt < 1965 or yearInt > 1995:
        print("Error: year must be between 1965 and 1995")
        sys.exit(1)
        
    inFile = f"{base}/json/Cooked/{year}.FIX.json"

    if args.output:
        outDir = f"{base}/Study"
        if not os.path.exists(outDir):
            os.makedirs(outDir)
            
        outFile = f"{outDir}/{year}.txt"
        outFP = open(outFile, 'w')

    if not args.quiet:
        print(f"\nYear: {year}\n")

    if args.output:
        outFP.write(f"\nYear: {year}\n")
    
    with open(inFile, 'r') as fp:
        jData = json.load(fp)

    Shows = jData['db_rest']['fetchArtistYear']['shows']
    showCount = len(Shows)
    
    insertCount = 0
    conn = sqlite3.connect(dbFile)
    with conn:
        cur = conn.cursor()

        for x in range(showCount):
            D['rec_id'] = "GDS-{}".format(uuid.uuid4())
            index = f"key_{x}"
            show = Shows[index]
            D['name'] = show['name']
            D['artist_key'] = show['artist_key']
            D['shows_key'] = show['shows_key']
            
            D['showdate'] = show['showdate']
            bits = D['showdate'].split('/')
            D['show_month'] = bits[0]
            D['show_day'] = bits[1]
            
            D['venue'] = MRSU.cleanStringForHTML(show['venue'])
            D['city'] = MRSU.cleanStringForHTML(show['city'])
            D['state'] = show['state']

            setList = ['set1', 'set2', 'set3']
            for entry in setList:
                tmpList = show[entry]
                anotherList = []
                for entry2 in tmpList:
                    anotherList.append(MRSU.cleanStringForHTML(entry2))
                D[entry] = anotherList
                    
            D['comment'] = MRSU.cleanStringForHTML(show['comment'])
            D['lastupdate'] = show['lastupdate']
            D['showyear'] = show['showyear']
            D['showsuserid'] = show['showsuserid']

            query = ("insert into setlists ( "
                     " rec_id,  band, artist_key, show_key, "
                     " show_date, venue, city, state_abbr, "
                     " set_1, set_2, set_3, comment, "
                     " last_update, show_year, show_user_id, "
                     " show_month, show_day) "
                     " values ( \"{}\", \"{}\", \"{}\", \"{}\", "
                     " \"{}\", \"{}\", \"{}\", \"{}\", "
                     " \"{}\", \"{}\", \"{}\", \"{}\", "
                     " \"{}\", \"{}\", \"{}\", \"{}\", \"{}\") ;"
                     .format(D['rec_id'], D['name'], D['artist_key'], 
                             D['shows_key'], D['showdate'], D['venue'], 
                             D['city'], D['state'], D['set1'], D['set2'], 
                             D['set3'], D['comment'], D['lastupdate'], 
                             D['showyear'], D['showsuserid'],
                             D['show_month'], D['show_day']))

            if not args.quiet:
                print(f"\n#\n# Key: {index}\n# -----------------------------------\n")
                print(query)

            if args.output:
                outFP.write(f"\n#\n# Key: {index}\n# -----------------------------------\n")
                outFP.write(query)

            if args.insert:
                print(f"Key: {index}")
                cur.execute(query)
                insertCount += 1

            if x == (showCount - 1):
                i = 0
            # End of for loop
        # End of with

    if args.output:
        outFP.close()

    conn.commit()
    cur.close()
    conn.commit()
    
    sys.exit(0)
    # End of main

if __name__ == '__main__':
    main()
