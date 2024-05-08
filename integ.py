import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import re
from tkinter import ttk
import analyzer
import promptgen

class UIClass:
    def __init__(self, a, promptgen):
        #objs 
        self.promptgen = promptgen
        self.analyzer = a
        #tk
        self.root = tk.Tk()
        self.WIDTH = 1500
        self.HEIGHT = 700
        self.PANELWIDTH = 350
        self.left_panel = tk.Frame(self.root, width=self.WIDTH/2, height=self.HEIGHT)
        self.right_panel = tk.Frame(self.root, width=self.WIDTH/2, height=self.HEIGHT)
        self.tab_control = ttk.Notebook(self.right_panel)
        self.tab1 = ttk.Frame(self.tab_control)
        self.tab2 = ttk.Frame(self.tab_control)
 
        #content
        self.additions = []
        self.essay = ""
        self.selected_sentence = "Click on any highlighted sentence to see your error"
        self.title1 = ttk.Label(self.tab1, text=self.selected_sentence, font=('Times New Roman', 18))
        self.matched_errors = []
        self.matched_sentences = []
        #run stuff
        self.create_ui()

    ### manage UI here ### 
    def create_ui(self):
        self.root.title("Essay Annihilator")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        self.root.resizable(False, False)

        ### LEFT PANEL ###
        self.left_panel.grid_propagate(False)
        self.left_panel.pack(side='left', fill='both', expand=True)
        self.text_area = ScrolledText(self.left_panel, wrap=tk.WORD, bg="white", font=('Times New Roman', 18), foreground="black")
        self.text_area.pack(padx=10, pady=10, fill='both', expand=True)

        ### RIGHT PANEL ###
        self.right_panel.pack(side='right', fill='both', expand=True)
        self.right_panel.grid_propagate(False)

        # Add tabs
        self.tab_control.add(self.tab1, text='Analyze')
        self.tab_control.add(self.tab2, text='Add to Model')
        self.tab_control.pack(expand=1, fill='both')

        # First tab
        ttk.Label(self.tab1, text="Analyze", font=('Times New Roman', 18)).pack(pady=10)
        tk.Button(self.tab1, text='Upload Text File', bg="lightgray", fg="black", highlightbackground='black',
                  font=('Times New Roman', 18), command=lambda: self.upload_file(self.text_area)).pack(pady=25, padx=20)
        tk.Button(self.tab1, text='Analyze Text', bg="lightgray", fg="black", highlightbackground='black',
                  font=('Times New Roman', 18), command=lambda: self.analyze_text(self.text_area)).pack(pady=10, padx=20)
        up_button = tk.Button(self.tab1, text="👍", command=self.feedback())
        up_button.pack(side=tk.LEFT, padx=10)

        # Add text entry to first tab
        ttk.Label(self.tab1, text="Feedback", font=('Times New Roman', 18)).pack(pady=10)
        self.feedback_entry = tk.Entry(self.tab1, font=('Times New Roman', 14), width=20)
        self.feedback_entry.pack(pady=50)
        self.submit_button = tk.Button(self.tab1, text="Submit", command=self.submit_feedback)
        self.submit_button.pack()

        # Create the "Thumbs Down" button
        down_button = tk.Button(self.tab1, text="👎", command=self.feedback())
        down_button.pack(side=tk.LEFT, padx=10)
        self.title1.pack(pady=20)

        # Second tab
        ttk.Label(self.tab2, text="Add to the model", font=('Times New Roman', 18)).pack(pady=10)
        
        ### TAGS FRAME ###
        self.tags_frame = tk.Frame(self.tab2, bg='white')
        self.tags_frame.pack(fill='both', expand=True, padx=20, pady=20)

        ### PHRASE ENTRY AND BUTTON ###
        self.phrase_entry = tk.Entry(self.tab2, font=('Times New Roman', 14), width=20)
        self.phrase_entry.pack(pady=10)
        self.add_button = tk.Button(self.tab2, text="Add Tag", command=self.add_tag)
        self.submit_button = tk.Button(self.tab2, text="Submit", command=self.submit)
        self.add_button.pack()
        self.submit_button.pack()
        
        self.root.mainloop()
    
    def submit_feedback(self):
        feedback = self.feedback_entry.get()
        if feedback:
            self.promptgen.add_bad_example(feedback, self.selected_sentence)
            self.feedback_entry.delete(0, tk.END)


    def submit(self):
        print('submit')

    def feedback(self):
        print("hello!")
        print('self.selected sentence')

    def add_tag(self):
        phrase = self.phrase_entry.get()
        if phrase:
            tag_frame = tk.Frame(self.tags_frame, bg="lightblue")
            tag_label = ttk.Label(tag_frame, text=phrase, background="lightblue")
            tag_label.pack(side='left', padx=5)
            remove_btn = ttk.Button(tag_frame, text="×", width=2, command=lambda f=tag_frame: self.remove_tag(f))
            remove_btn.pack(side='right')
            tag_frame.pack(pady=5, padx=5)
            self.phrase_bubbles.append(tag_frame)
            self.phrase_entry.delete(0, tk.END) 

    def remove_tag(self, frame):
        frame.destroy()
        self.phrase_bubbles.remove(frame) 

    ### upload file as a .txt and read ### 
    def upload_file(self, text_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.essay = content
                text_widget.delete('1.0', tk.END)
                text_widget.insert(tk.END, content)

    ### highlight sentences here ### 
    def analyze_text(self, text_widget):
        results = self.analyzer.process_data(self.essay)
        pattern = r'\d+\.\s+"(.*?)"\s*(.*?)(?:\n|$)'
        
        ### find sentences in the text ###
        matches = re.findall(pattern, results, re.DOTALL)
        for match in matches:
            sentence, after_sentence = match
            self.matched_sentences.append(sentence)
            self.matched_errors.append(after_sentence)

        ### tag to highlight ###
        for index, sentence in enumerate(self.matched_sentences):
            start_index = self.essay.find(sentence)
            if start_index != -1:
                if not start_index == 0:
                    end_index = start_index + len(sentence)
                    start_position = text_widget.index(f"1.0+{start_index}c")
                    end_position = text_widget.index(f"1.0+{end_index}c")
                    tag_name = f"highlight_{index}"
                    text_widget.tag_add(tag_name, start_position, end_position)
                    text_widget.tag_config(tag_name, background='yellow', foreground='black')

                    def on_click(event, s=sentence):
                        self.selected_sentence = sentence
                        idx = self.matched_sentences.index(s)
                        error = self.matched_errors[idx]
                        self.title1.config(text=error)
                        self.root.update_idletasks()

                    text_widget.tag_bind(tag_name, "<Button-1>", on_click)
            else:
                print("nooooo")
                print("+" + sentence + "+")


if __name__ == "__main__":
    promptgen = promptgen.PromptGen()
    analysis = analyzer.Analyzer(promptgen)
    promptgen.check()
    ui = UIClass(analysis, promptgen)
    ui.create_ui()
