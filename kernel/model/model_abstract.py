from abc import ABC, abstractmethod
from kernel.transformers.transformer_abstract import TransformerAbstract


class ModelAbstract(ABC):
    def __init__(self, model_path, model_category, transformer: TransformerAbstract):
        self.model_path = model_path
        self.model_category = model_category
        self.model = self.upload_model()
        self.transformer = transformer

    @abstractmethod
    def upload_model(self):
        ...

    def get_features(self, df_features):
        module = df_features['Module']
        df_help = df_features.drop(['Module'], axis=1)
        df_help = df_help.cumsum().fillna(method='ffill')
        df_help['Module'] = module
        df_help = df_help.tail(1)
        return self.transformer.transform(df_help)

    @abstractmethod
    def get_prediction(self, df_features):
        ...

    def need_prediction(self, prefix) -> bool:
        return prefix == self.model_category
