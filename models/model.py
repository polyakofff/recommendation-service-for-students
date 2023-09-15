from abc import ABC, abstractmethod


class Model(ABC):

    def __init__(self, category, path):
        self.category = category
        self.path = path
        self.model = self.load_model()

    @abstractmethod
    def load_model(self):
        pass

    def prepare_data(self, df):
        pass

    def get_prediction(self, df):
        x = self.prepare_data(df)

