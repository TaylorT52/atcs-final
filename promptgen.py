import pandas as pd

class PromptGen():
    def __init__(self):
        self.file = "data/errors.csv"
        self.df = pd.read_csv(self.file)

    def read_csv(self):
        print('reading csv ... ')
        print(self.df.head())

    def add_error(self):
        print("add error")