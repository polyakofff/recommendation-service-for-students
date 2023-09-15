from models.model import Model
import catboost as cb


class CbmModel(Model):

    def load_model(self):
        model = cb.CatBoostClassifier()
        model.load_model(self.path)
        return model
