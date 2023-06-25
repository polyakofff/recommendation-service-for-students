from abc import abstractmethod


class TransformerAbstract:

    @abstractmethod
    def transform(self, df):
        ...