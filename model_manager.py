from models.cbm_model import CbmModel
from models.pkl_model import PklModel
from models.model_category import ModelCategory as MC

class ModelManager:

    def __init__(self):
        self.models = {
            ('fen', 'mag'): PklModel(MC.FEN_MAG, 'models/fen_mag.pkl'),
            ('miem', 'mag'): CbmModel(MC.MIEM_MAG, 'models/model_miem_mag.cbm')
        }

    def get_model(self, faculty, degree):
        return self.models[(faculty, degree)]
