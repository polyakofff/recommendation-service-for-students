from kernel.model.model_abstract import ModelAbstract
from constant.model_categories import FEN_MAG
from kernel.data_info import DataInfo
class FenMagModel(ModelAbstract):
    @property
    def model_category(self):
        return FEN_MAG

    def upload_model(self):
        model = cb.CatBoostClassifier()
        model.load_model(self.model_path)
        return model

    def get_features(self, dto_in: DataInfo):
        return []