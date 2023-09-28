FEN_MAG = 'fen_mag'
MIEM_MAG = 'miem_mag'
FKN_BAC = 'fkn_bac'

PREFIX_MAP = {
    FEN_MAG: 'ФЭН Магистратура',
    MIEM_MAG: 'МИЭМ Магистратура',
    FKN_BAC: 'ФКН Бакалавриат'
}

def create_prefix(faculty, degree):
    return f'{faculty}_{degree}'
