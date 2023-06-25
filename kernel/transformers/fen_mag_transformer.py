import pandas as pd
from kernel.transformers.transformer_abstract import TransformerAbstract


class FenMagTransformer(TransformerAbstract):

    def transform(self, df):
      df["ID"] = [0]
      new_df = pd.concat([df, (~df.isnull()).astype(int).add_prefix("bool")], axis=1, join='inner')
      new_df = new_df.fillna(0)
      new_df = new_df.drop(['boolModule', 'boolID'], axis=1)
      return new_df