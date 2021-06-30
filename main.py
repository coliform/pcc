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
with open("drafts/file.c","rb") as f:
    while b:=f.read(1):
        b = b[0]
        if b not in ascii_permitted_bytes: b = ord('?')
        source += chr(b)
# 1.2 - replace trigraph characters
for (key,value) in trigraphs.items(): source = source.replace(key,value)


# PHASE 2
# 2.1 - replace \\n with nothing
source = remove_backslash_newl(source)

# PHASE 3
source = pcc_utils.remove_comments(source)
while segment := find_next_string(source):
    if segment[0]==-1: break
    (start_i,end_i) = segment
    literal_table += source[start_i:end_i]
    source = source[:start_i] + pcc_literal_token + source[end_i+1:]
source = remove_excessive_whitespace(source)

print(source)


'''
Compound statements belong to their adjacent left side, until we see a semicolon 
Expression statements are followed by a semicolon
'''

def read_scope(raw):
    scope = pcc_scope()
    i = 0
    l = len(raw)
    raw_statement = ""
    while i < l:
        i_end = find_statement_end(raw,i)
        if i_end == -1: die("Bad scope")
        raw_statement = raw[i:i_end]
        i+=1

    

program = read_scope(source)
