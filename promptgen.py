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
        self.bad_sentences = []
        self.feedback_list = []
        self.feedback_path = "data/feedback.txt"

        self.goal_basic = f"Return exact sentences that state the existence of value without specifying what is important, containing the following phrases {', '.join(self.tvw)}. Don't extrapolate meaning."

    def generate_goal(self):
        goal = self.goal_basic + " Here are example sentence evaluations for context: "
        with open(self.feedback_path, 'r') as file:
            for line in file:
                goal += line.strip()
        return goal
            
    def remove_nan(self, list):
        return [x for x in list if str(x) != 'nan']
    
    def add_error(self):
        print("add error")

    def add_bad_example(self, feedback, selected_sentence):
        with open(self.feedback_path, 'a') as file:
            file.write(f"{selected_sentence}. This sentence should NOT be highlighted because {feedback}" + '\n') 

    def check(self):
        print(self.tvw)
        print(self.generalizations)
        print(self.weak_verbs)
        print(self.nominalizations)

if __name__ == "__main__":
    gen = PromptGen()
    gen.check()
