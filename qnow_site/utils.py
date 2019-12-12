# DEF - Converte date US para PT-BR
def convert_date_to_br(date_value):
    if not date_value: 
        return null
    date_text = str(date_value).split('-')
    return '/'.join(list(reversed(date_text)))
