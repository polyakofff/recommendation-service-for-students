from kernel.model.catboost_model import CatboostModel
from constant.model_categories import MIEM_MAG, FEN_MAG
from kernel.model.pickle_model import PickleModel
from kernel.transformers.fen_mag_transformer import FenMagTransformer

class ModelRunner:

    def __init__(self):
        self.model_register = [
            # CatboostModel('./models/model_miem_mag.cbm', MIEM_MAG)
            PickleModel('./models/model_fen_mag.pkl', FEN_MAG, FenMagTransformer())
        ]

    def get_prediction(self, df_features, prefix):
        models_for_run = [model for model in self.model_register if model.need_prediction(prefix)]

        return [model.get_prediction(df_features) for model in models_for_run]
