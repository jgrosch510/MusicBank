#!/usr/bin/env python
# -*- mode: python -*-
# -*- coding: utf-8 -*-

import os, sys

def main(argv, argc):

    a = argv
    b = argc

    if argc == 1:
        printMasterHelp()

    # Add    - MBAdd.py
    # Check  - MBCheck.py
    # Delete - MBDelete.py
    # List   - MBList.py
    # Manage - MBManage.py
    # Rip    - MBRip.py
    # Update - MBUpdate.py
    
    sys.exit(0)
    # End of main

def printMasterHelp():
    print("RTFM")

    return

if __name__ == '__main__':
    main(sys.argv, len(sys.argv))

    
