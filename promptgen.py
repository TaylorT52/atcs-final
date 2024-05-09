#authors @ taylor tam & cody kletter
#manages phrases, example sentences, and updates task & goal for the model

import pandas as pd
import csv

class PromptGen():
    def __init__(self):
        #paths
        self.file = "data/errors.csv"
        self.feedback_path = "data/feedback.txt"
        #get csv
        self.df = pd.read_csv(self.file)
        #get manage parts of csv
        self.tvw = self.df["tvw"].tolist()
        self.generalizations = self.df["Generalizations"].tolist()
        self.weak_verbs = self.df["Weak verbs"].tolist()
        self.nominalizations = self.df["Nominalization"].tolist()
        self.remove_nan_all()
        self.additional_phrases = []

    #removes any nans from csv
    def remove_nan_all(self):
        self.generalizations = self.remove_nan(self.generalizations)
        self.tvw = self.remove_nan(self.tvw)
        self.weak_verbs = self.remove_nan(self.weak_verbs)
        self.nominalizations = self.remove_nan(self.nominalizations)

    #generates the model task, updates if any tvw's have been added
    def generate_task(self):
        return f"Return the exact sentences that declare the existence or necessity of importance, without detailing the object or subject of that importance. The sentences MUST contain the following phrases {', '.join(self.tvw)} in the given text:"

    #generates the model goal, including added phrases, tvw, and any example sentences
    def generate_goal(self):
        goal = f"Return exact sentences that state the existence of value without specifying what is important, containing the following phrases {', '.join(self.tvw)}, {', '.join(self.additional_phrases)}. Don't extrapolate meaning." + " Here are example sentence evaluations for context: "
        with open(self.feedback_path, 'r') as file:
            for line in file:
                goal += line.strip()
        return goal
            
    def remove_nan(self, list):
        return [x for x in list if str(x) != 'nan']
    
    #adds phrases that should be marked 
    def add_error(self, ls_phrases):
       for phrase in ls_phrases:
           if phrase not in self.additional_phrases:
               self.additional_phrases.append(phrase)

    #adds sentences that were poorly marked & submitted with feedback
    def add_bad_example(self, feedback, selected_sentence):
        with open(self.feedback_path, 'a') as file:
            file.write(f"{selected_sentence}. This sentence should NOT be highlighted because {feedback}" + '\n') 

    def check(self):
        print(self.tvw)
        print(self.generalizations)
        print(self.weak_verbs)
        print(self.nominalizations)