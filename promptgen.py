import pandas as pd

class PromptGen():
    def __init__(self):
        self.file = "data/errors.csv"
        self.df = pd.read_csv(self.file)
        self.tvw = self.df["tvw"].tolist()
        self.generalizations = self.df["Generalizations"].tolist()
        self.weak_verbs = self.df["Weak verbs"].tolist()
        self.nominalizations = self.df["Nominalization"].tolist()

    def add_error(self):
        print("add error")

    def check(self):
        print(self.tvw)
        print(self.generalizations)
        print(self.weak_verbs)
        print(self.nominalizations)