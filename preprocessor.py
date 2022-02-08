import pandas as pd


def preprocess(df, df2):
    df = df[df['Season'] == "Summer"]
    df = df.merge(df2, how="left", on="NOC")
    df.drop_duplicates(inplace=True)
    df = pd.concat([df, pd.get_dummies(df['Medal'])], axis=1)
    return df
