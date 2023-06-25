from kernel.model.model_abstract import ModelAbstract
import catboost as cb


class CatboostModel(ModelAbstract):
    def upload_model(self):
        model = cb.CatBoostClassifier()
        model.load_model(self.model_path)
        return model
