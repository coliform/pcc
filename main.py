#!/usr/bin/env python3

# raise Exception for valid compilation errors
# assert for compiler issues

import pcc_structures
import pcc_utils
import pcc_constants


# PHASE 1
# 1.1 - read file
s = ""
with open("file.c","r") as f: s=f.read()
# 1.2 - replace trigraph characters
for key,value in pcc_constants.trigraphs: s = s.replace(key,value)


# PHASE 2
# 2.1 - replace \\n with nothing
s = s.replace("\\\n","")


# PHASE 3
s = pcc_utils.remove_comments(s)
