#!/usr/bin/env python3

import re
import os
import sys

if len(sys.argv) == 1:
    print("usage: {} fun_directory".format(sys.argv[0]))
    sys.exit(1)

FILE_NO = r"file(\d+)"
FILE_NO_REG = re.compile(FILE_NO)

ordered = dict()

for root, dirs, files in os.walk(sys.argv[1]):
    for pcap_file in files:
        f = open(os.path.join(root, pcap_file), "r")
        tmp = f.read()
        matches = FILE_NO_REG.search(tmp)
        no = matches.group(1)
        ordered[int(no)] = tmp
        f.close()

for i in range(1, len(files) + 1):
    print(ordered[i])
