from kernel.transformers.transformer_abstract import TransformerAbstract
import pandas as pd


class FknMagTransformer(TransformerAbstract):

    def transform(self, df):
        df_with_new_features = pd.concat([df, (~df.isnull()).astype(int).add_prefix("is_take_")], axis=1, join='inner')
        df_with_new_features = df_with_new_features.fillna(0)
        df_with_new_features = df_with_new_features.drop(['is_take_Module'], axis=1)
        return df_with_new_features