import numpy as np
import pandas as pd

class Enviroment:
    def __init__(self, gen_random: bool = True, file_path: str = None):
        if gen_random:
            pass
        else:
            self.map = pd.read_csv(file_path).to_numpy()
