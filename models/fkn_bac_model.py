from models.model import Model
import catboost as cb


class FknBacModel(Model):

    def load_model(self):
        model0 = cb.CatBoostClassifier()
        model0.load_model(self.path)
        return model0

    def get_features(self, df):
        df['ID'] = 0
        df['Year'] = (df['Module'] - 1) // 4 + 1
        subjects = df.columns.drop(['ID', 'Module', 'Year'])
        df[subjects] = df.groupby(['ID', 'Year'])[subjects].transform(lambda by_id: by_id.cumsum().ffill())
        taken = (~df[subjects].isna()).astype(int).add_prefix('Taken_')
        df[subjects] = df[subjects].fillna(0)
        df = df.join(taken)
        df = df.reindex(columns=['Module', 'Year'] + subjects.tolist() + taken.columns.tolist())
        return df.tail(1)

    def feature_names(self):
        return self.model0.feature_names_
