import pandas as pd
from kernel.transformers.transformer_abstract import TransformerAbstract


class MiemMagTransformer(TransformerAbstract):
    def transform(self, data):
        # Joining the "Taken" columns
        taken_cols = (~data.isnull()).drop(['Module'], axis=1).astype(int).add_prefix('Taken_')
        data = data.join(taken_cols)

        # Applying one-hot encoding
        module_encoded = pd.get_dummies(data['Module'], prefix='Module')
        data_encoded = pd.concat([data, module_encoded], axis=1)
        data_encoded.drop(columns=['Module'], inplace=True)

        return data_encoded
