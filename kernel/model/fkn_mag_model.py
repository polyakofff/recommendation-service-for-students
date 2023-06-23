from kernel.model.model_abstract import ModelAbstract
from constant.model_categories import FKN_MAG
import catboost as cb
from kernel.data_info import  DataInfo

class FknMagModel(ModelAbstract):
    @property
    def model_category(self):
        return FKN_MAG

    def upload_model(self):
        model = cb.CatBoostClassifier()
        model.load_model(self.model_path)
        return model

    def get_features(self, dto_in: DataInfo):
        return []