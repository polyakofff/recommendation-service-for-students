from kernel.model.model_abstract import ModelAbstract
import pickle

from sklearn.ensemble import RandomForestClassifier


class PickleModel(ModelAbstract):
    def upload_model(self):
        with open(self.model_path, 'rb') as f:
            model = pickle.load(f)
        return model

    def get_prediction(self, df_features):
        x = self.get_features(df_features)
        x = x.reindex(list(self.model.feature_names_in_), axis=1)
        return list(list(self.model.predict_proba(x))[0])
