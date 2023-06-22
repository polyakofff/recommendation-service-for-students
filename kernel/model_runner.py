from kernel.model.miem_mag_model import MIEMMagModel
from kernel.data_info import DataInfo
class ModelRunner:

    def __init__(self, db_api):
        self.model_register = [
            MIEMMagModel(db_api, './models/model_miem_mag.cbm')
        ]

    def get_prediction(self, dto_in: DataInfo):
        models_for_run = [model for model in self.model_register if model.need_prediction(dto_in)]

        return [model.get_prediction(dto_in) for model in models_for_run]

