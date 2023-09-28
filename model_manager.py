from models.model_category import FEN_MAG, MIEM_MAG, FKN_BAC, create_prefix
from models.fen_mag_model import FenMagModel
from models.miem_mag_model import MiemMagModel
from models.fkn_bac_model import FknBacModel


class ModelManager:

    def __init__(self):
        self.models = {
            FEN_MAG: FenMagModel('models/fen_mag.pkl'),
            MIEM_MAG: MiemMagModel('models/miem_mag.cbm'),
            FKN_BAC: FknBacModel('models/fkn_bac.cbm')
        }

    def get_model(self, faculty, degree):
        prefix = create_prefix(faculty, degree)
        return self.models[prefix]
