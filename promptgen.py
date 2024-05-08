import pandas as pd
import csv

class PromptGen():
    def __init__(self):
        self.file = "data/errors.csv"
        self.feedback_path = "data/feedback.txt"
        self.df = pd.read_csv(self.file)
        self.tvw = self.df["tvw"].tolist()
        self.tvw = self.remove_nan(self.tvw)
        self.generalizations = self.df["Generalizations"].tolist()
        self.generalizations = self.remove_nan(self.generalizations)
        self.weak_verbs = self.df["Weak verbs"].tolist()
        self.weak_verbs = self.remove_nan(self.weak_verbs)
        self.nominalizations = self.df["Nominalization"].tolist()
        self.nominalizations = self.remove_nan(self.nominalizations)
        f = open(self.feedback_path, "r")
        self.feedback = f.read()
    def remove_nan(self, list):
        return [x for x in list if str(x) != 'nan']
    
    def add_error(self):
        print("add error")

    def add_bad_example(self, feedback, selected_sentence):
        f = open(self.feedback_path, "a")
        f.write(f"Example: '{selected_sentence}' is an incorrectly identified error because {feedback}. ")
        f.close()
        print(feedback)

    def check(self):
        print(self.tvw)
        print(self.generalizations)
        print(self.weak_verbs)
        print(self.nominalizations)

if __name__ == "__main__":
    gen = PromptGen()
    gen.check()
