from models.model import Model
import pickle
import pandas as pd


class FenMagModel(Model):

    def load_model(self):
        with open(self.path, 'rb') as f:
            model0 = pickle.load(f)
        return model0

    def get_features(self, df):
        cum = df.drop('Module', axis=1).cumsum().ffill()
        df = pd.concat([df['Module'], cum], axis=1)
        df = df.tail(1)

        df["ID"] = [0]
        new_df = pd.concat([df, (~df.isnull()).astype(int).add_prefix("bool")], axis=1, join='inner')
        new_df = new_df.fillna(0)
        new_df = new_df.drop(['boolModule', 'boolID'], axis=1)
        return new_df

    def feature_names(self):
        return self.model0.feature_names_in_
