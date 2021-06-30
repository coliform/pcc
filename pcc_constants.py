import pcc_utils

whitespace = [' ', '\t', '\r', '\n']

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
    '??)':']'
} # TODO: incomplete