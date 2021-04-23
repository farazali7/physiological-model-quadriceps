import pandas as pd


def load_model_configuration(file):
    df = pd.read_csv(file)
    config = {}
    for column in df:
        value = df[column].dropna().to_numpy()
        if len(value) == 1:
            value = value.item()
        config[column] = value
    return config
