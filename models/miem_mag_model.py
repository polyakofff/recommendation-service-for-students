from models.model import Model
import catboost as cb
import pandas as pd


class MiemMagModel(Model):

    def load_model(self):
        model0 = cb.CatBoostClassifier()
        model0.load_model(self.path)
        return model0

    def get_features(self, df):
        cum = df.drop('Module', axis=1).cumsum().ffill()
        df = pd.concat([df['Module'], cum], axis=1)
        data = df.tail(1)

        # Joining the "Taken" columns
        taken_cols = (~data.isnull()).drop(['Module'], axis=1).astype(int).add_prefix('Taken_')
        data = data.join(taken_cols)

        # Applying one-hot encoding
        module_encoded = pd.get_dummies(data['Module'], prefix='Module')
        data_encoded = pd.concat([data, module_encoded], axis=1)
        data_encoded.drop(columns=['Module'], inplace=True)

        return data_encoded

    def feature_names(self):
        return self.model0.feature_names_
