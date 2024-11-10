import pandas as pd
import numpy as np
import os

class DatasetLoader:
    def __init__(self, csv_path: str):
        if os.path.exists(csv_path):
            self.df = pd.read_csv(csv_path)
        else:
            raise ValueError(f"### File {csv_path} does not exist ###")

    @property
    def data(self):
        return self.df.iloc[:, :7].to_numpy()

    @property
    def target(self):
        return np.squeeze(self.df.iloc[:, 7:].to_numpy(), axis=-1)

