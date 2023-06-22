from abc import ABC, abstractmethod
from kernel.data_info import DataInfo

class ModelAbstract(ABC):
    def __init__(self, db_api, model_path):
        self.db_api = db_api
        self.model_path = model_path
        self.model = self.upload_model()


    @property
    @abstractmethod
    def model_category(self):
        ...

    @abstractmethod
    def upload_model(self):
        ...

    @abstractmethod
    def get_features(self, dto_in: DataInfo):
        return self.model.feature_names_

    def get_prediction(self, dto_in: DataInfo):
        x = self.get_features(dto_in)
        return self.model.feature_names_

    def need_prediction(self, dto_in: DataInfo) -> bool:
        return dto_in.model_category == self.model_category
