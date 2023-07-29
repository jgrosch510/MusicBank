#!/usr/bin/env python3

import os, sys
from MusicBank import MB_db_util as MBDU

def main():
    dbParamFile = '/usr/local/site/etc/moosedb-ecalendar-db.json'

    D = MBDU.connectToDatabaseJson(dbParamFile)

    sys.exit(0)
    #

if __name__ == '__main__':
    main()
    
    
