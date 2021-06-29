import pcc_utils
from pcc_structures import pcc_type_table

whitespace = [' ', '\t', '\r', '\n']

pcc_literal_token = '$'
        

pcc_types = pcc_type_table()
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