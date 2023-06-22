from kernel.model.model_abstract import ModelAbstract
from constant.model_categories import MIEM_MAG
from kernel.data_info import DataInfo
import catboost as cb

class MIEMMagModel(ModelAbstract):

    @property
    def model_category(self):
        return MIEM_MAG

    def upload_model(self):
        model = cb.CatBoostClassifier()
        model.load_model(self.model_path)
        return model

    def get_features(self, dto_in: DataInfo):
        return []