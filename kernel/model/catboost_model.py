from kernel.model.model_abstract import ModelAbstract
import catboost as cb


class CatboostModel(ModelAbstract):
    def upload_model(self):
        model = cb.CatBoostClassifier()
        model.load_model(self.model_path)
        return model

    def get_prediction(self, df_features):
        x = self.get_features(df_features)
        x = x.reindex(list(self.model.feature_names_), axis=1)
        return list(list(self.model.predict_proba(x))[0])
