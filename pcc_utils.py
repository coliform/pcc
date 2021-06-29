import string
import re

def is_lambda(v):
  LAMBDA = lambda:0
  return isinstance(v, type(LAMBDA)) and v.__name__ == LAMBDA.__name__

def is_str(v):
    return type(v)==str

def is_int(v):
    return type(v)==int

def is_valid_identifier(v):
    return v.isidentifier() #apparently built into python

class FileStream:
    def __init__(self, path):
        self._f = open(path,'rb')
    def __iter__(self):
        return self
    def __next__(self):
        b = self._f.read(1)
        if not b: raise StopIteration
        return b

def die(details):
    print("Failed to compile due to:\n{}".format(details))
    exit()

def get_string_end(s,i):
    l=len(s)
    if s[i]!='"' or (i>0 and s[i-1]=='\\'): return i
    i+=1
    while i<l and (s[i]!='"' or s[i-1]=='\\'): i+=1
    if i==l: die("Unterminated string")
    return i

def remove_comments_single(raw):
    s = ""
    l = len(raw)
    i = 0

    while i < l:
        j=get_string_end(raw,i)
        s += raw[i:j]
        i=j
        if i<l-1 and raw[i]=="/" and raw[i+1]=='/':
            while i<l and raw[i]!='\n': i+=1
            continue
        s += raw[i]
        i+=1
    return s

def remove_comments_multi(raw):
    s = ""
    l = len(raw)
    i = 0

    while i < l:
        j=get_string_end(raw,i)
        s += raw[i:j]
        i=j
        if raw[i]=="/" and i<l-1 and raw[i+1]=='*':
            i+=2
            while i<l-1 and not (raw[i]=='*' and raw[i+1]=='/'): i+=1
            if i==l-1 and raw[i+1]!='/': die("Unterminated multiline comment")
            i+=2
            continue
        s += raw[i]
        i+=1
    return s

def remove_comments(raw):
    return remove_comments_multi(remove_comments_single(raw))

def find_first_not_in_string(haystack, needle):
    l = len(haystack)
    i = 0
    while i < l:
        if haystack[i] == needle: return i
        if haystack[i] == '\'':
            while i<l and haystack[i] != '\'': i+=1
        if haystack[i] == '\"':
            while i<l and haystack[i] != '\"': i+=1
        i+=1
    return -1

def find_next_not_in_string(haystack, needle, start):
    l = len(haystack)
    assert(start >= 0 and start < l)
    in_string = False
    i = 0
    while i <= start:
        in_string ^= haystack[i] == '\'' or haystack[i] == '\"'
        i += 1
    while in_string and i < l:
        pass
    while i >= 0:
        if haystack[i] == '\'' or haystack[i] == '\"': break
        i -= 1
    if i==-1: return start+find_first_not_in_string(haystack[start:],needle)
    else: return i+find_first_not_in_string()