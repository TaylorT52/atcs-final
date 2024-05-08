import pandas as pd
import csv

class PromptGen():
    def __init__(self):
        self.file = "data/errors.csv"
        self.df = pd.read_csv(self.file)
        self.tvw = self.df["tvw"].tolist()
        self.tvw = self.remove_nan(self.tvw)
        self.generalizations = self.df["Generalizations"].tolist()
        self.generalizations = self.remove_nan(self.generalizations)
        self.weak_verbs = self.df["Weak verbs"].tolist()
        self.weak_verbs = self.remove_nan(self.weak_verbs)
        self.nominalizations = self.df["Nominalization"].tolist()
        self.nominalizations = self.remove_nan(self.nominalizations)
        self.bad_sentences = []
        self.feedback_list = []
    def remove_nan(self, list):
        return [x for x in list if str(x) != 'nan']
    
    def add_error(self):
        print("add error")

    def add_bad_example(self, feedback, selected_sentence):
        with open(self.file, 'w') as file:
            csvwriter = csv.writer(file)
            csvwriter.writerow(selected_sentence + "," + feedback)
        print(feedback)

    def check(self):
        print(self.tvw)
        print(self.generalizations)
        print(self.weak_verbs)
        print(self.nominalizations)
        print(self.feedback_list)

if __name__ == "__main__":
    gen = PromptGen()
    gen.check()
