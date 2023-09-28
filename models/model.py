from abc import ABC, abstractmethod
import pandas as pd


class Model(ABC):

    def __init__(self, path):
        self.path = path
        self.model0 = self.load_model()

    @abstractmethod
    def load_model(self):
        pass

    @abstractmethod
    def get_features(self, df):
        pass

    @abstractmethod
    def feature_names(self):
        pass

    def get_prediction(self, df):
        x = self.get_features(df)
        x = x.reindex(columns=self.feature_names())
        print(x)
        return self.model0.predict_proba(x)[0].tolist()

    def recommend(self, df, subjects_id_2_name, n):
        x = self.get_features(df)
        x = x.reindex(columns=self.feature_names())
        print(x)
        fi = pd.Series(self.model0.feature_importances_.tolist(), x.columns).sort_values(ascending=False)
        recs = []
        for f, i in fi.items():
            if f == 'ID' or f == 'Module' or f == 'Year':
                continue
            if f.startswith('bool') or f.startswith('Taken'):
                continue
            else:
                if int(x[f]) < 8:
                    recs.append(f'\'{subjects_id_2_name[f]}\' should be passed perfectly')
            if len(recs) == n:
                break
        return recs
