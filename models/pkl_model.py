from models.model import Model
import pickle


class PklModel(Model):

    def load_model(self):
        with open(self.path, 'rb') as f:
            model = pickle.load(f)
        return model
