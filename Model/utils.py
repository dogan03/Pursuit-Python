import pandas as pd
import numpy as np
def text_to_df(name):
    with open(f'Data/{name}/{name}.txt', 'r') as file:
        lines = file.readlines()
    uttered = []
    visible = []
    row = 0
    while row < len(lines):
        uttered.append(lines[row].split())
        visible.append(lines[row+1].split())
        row +=3
    return pd.DataFrame({
        "uttered" : uttered,
        "visible" : visible
    })


#From Data Directory get the csv as dict
def csv_to_dict(name):
    df = pd.read_csv(f'Data/{name[:len(name)-5]}/{name}.csv')
    train = {}

    for i in range(len(df)):
        train[df.iloc[i, 0]] = df.iloc[i, 1]
    return train