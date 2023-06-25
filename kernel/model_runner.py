from kernel.model.catboost_model import CatboostModel
from constant.model_categories import MIEM_MAG, FEN_MAG
from kernel.model.pickle_model import PickleModel
from kernel.transformers.fen_mag_transformer import FenMagTransformer
from db_api import DBOrm

class ModelRunner:

    def __init__(self, db_orm: DBOrm):
        self.db_orm = db_orm
        self.model_register = [
            # CatboostModel('./models/model_miem_mag.cbm', MIEM_MAG)
            PickleModel('./models/model_fen_mag.pkl', FEN_MAG, FenMagTransformer())
        ]

    def get_prediction(self, student_id):
        df_features, prefix = self.db_orm.get_features_for_student(student_id)

        models_for_run = [model for model in self.model_register if model.need_prediction(prefix)]

        return [model.get_prediction(df_features) for model in models_for_run], prefix
