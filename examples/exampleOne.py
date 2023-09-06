#!/usr/bin/env python3

import os, sys
from MusicBank import MB_db_util as MBDU
from MusicBank import MB_common as MBC

def main():
    dbParamFile = '/usr/local/site/etc/moosedb-ecalendar-db.json'
    RS = MBC.ReturnStatus
    
    D = MBDU.connectToDatabaseJson(dbParamFile)
    if D['status'] == RS.OK:
        dbConnect = D['data']

    cursor = dbConnect['cursor']
    conn = dbConnect['conn']
    
    conn.close()
    
    sys.exit(0)
    #

if __name__ == '__main__':
    main()
    
    
