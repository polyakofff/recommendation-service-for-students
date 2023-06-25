MIEM_MAG = 'miem_mag'
MIEM_BACH = 'miem_bach'
FKN_MAG = 'fkn_mag'
FKN_BACH = 'fkn_bach'
FEN_MAG = 'fen_mag'
FEN_BACH = 'fen_bach'

PREFIX_INFO = {
    'miem_mag': 'МИЭМ Магистратура',
    'fkn_mag': 'ФКН Магистратура',
    'miem_bach': 'МИЭМ Бакалавриат',
    'fkn_bach': 'ФКН Бакалавриат',
    'fen_mag': 'ФЭН Магистратура',
    'fen_bach': 'ФЭН Бакалавриат'
}

def prefix_creator(degree, faculcy):
    return  f'{faculcy}_{degree}'