#!/usr/bin/env python3

# raise Exception for valid compilation errors
# assert for compiler issues

from pcc_structures import *
from pcc_constants import *
import pcc_utils

type_table = pcc_type_table()
literal_table = pcc_literal_table()
operator_table = pcc_operator_table()


# PHASE 1
# 1.1 - read file
source = ""
with open("drafts/file.c","r") as f: source=f.read()
# 1.2 - replace trigraph characters
for (key,value) in trigraphs: source = source.replace(key,value)


# PHASE 2
# 2.1 - replace \\n with nothing
source = source.replace("\\\n","")


# PHASE 3
source = pcc_utils.remove_comments(source)
while segment := find_next_string(source):
    (start_i,end_i) = segment
    literal_table += source[start_i:end_i]
    source = source[:start_i] + pcc_literal_token + source[end_i+1:]
source = remove_excessive_whitespace(source)

print(source)