from abc import ABC, abstractmethod

class ModelAbstract(ABC):
    def __init__(self, model_path, model_category):
        self.model_path = model_path
        self.model_category = model_category
        self.model = self.upload_model()

    @abstractmethod
    def upload_model(self):
        ...

    def get_features(self, df_features):
        module = df_features['Module']
        df_help = df_features.drop(['Module'], axis=1)
        df_help = df_help.cumsum()
        df_help['Module'] = module
        return df_help.tail(1)

    def get_prediction(self, df_features):
        x = self.get_features(df_features)
        return self.model.feature_names_

    def need_prediction(self, prefix) -> bool:
        return prefix == self.model_category
