import pcc_utils

ascii_whitespace = [' ', '\t', '\v', '\r', '\n']
ascii_digits = ['0','1','2','3','4','5','6','7','8','9']
ascii_letters = list('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
ascii_punctuation = list('_\{\}\[\]#()<>%:;.?*+-/^&|~!=,\\\"\'')
ascii_permitted = ascii_whitespace + ascii_digits + ascii_letters + ascii_punctuation
ascii_permitted_bytes = bytes([ord(c) for c in ascii_permitted])

pcc_literal_token = '$'
        

alternative_tokens = {
    '<%':'{',
    '%>':'}',
    '<:':'[',
    ':>':']',
    '%:':'#',
    '%:%:':'##'
}

trigraphs = {
    '??<':'{',
    '??>':'}',
    '??(':'[',
    '??)':']',
    '??=':'#',
    '??/':'\\',
    '??\'':'^',
    '??!':'|',
    '??-':'~'
}