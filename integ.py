import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText
import re
from tkinter import ttk
import analyzer


class UIClass:
    def __init__(self, a):
        self.analyzer = a
        self.root = tk.Tk()
        self.WIDTH = 1500
        self.HEIGHT = 700
        self.PANELWIDTH = 350
        self.essay = ""
        self.selected_sentence = "Click on any highlighted sentence to see your error"
        self.dropdown_options = ["Option 1", "Option 2", "Option 3"]
        self.acceptable = [",", "-", ";", ":", "'", "’", " "]
        self.create_ui()

    def create_ui(self):
        self.root.title("Essay Annihilator")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")
        left_panel = tk.Frame(self.root, bg='white')
        left_panel.pack(side='left', fill='both', expand=True)
        self.text_area = ScrolledText(left_panel, wrap=tk.WORD, bg="white", font=('Times New Roman', 18), foreground="black")
        self.text_area.pack(padx=10, pady=10, fill='both', expand=True)
        right_panel = tk.Frame(self.root, bg='lightgray', width=self.PANELWIDTH)
        right_panel.pack(side='right', fill='both', expand=True)
        title0 = ttk.Label(right_panel, text="Analyze")
        title0.pack(pady=10)
        upload_button = tk.Button(right_panel, text='Upload Text File', bg="lightgray", fg="black", highlightbackground='black',
                                  font=('Times New Roman', 18), command=lambda: self.upload_file(self.text_area))
        upload_button.pack(pady=25, padx=20)
        analyze_button = tk.Button(right_panel, text='Analyze Text', bg="lightgray", fg="black", highlightbackground='black',
                                   font=('Times New Roman', 18), command=lambda: self.analyze_text(self.text_area))
        analyze_button.pack(pady=10, padx=20)
        title1 = ttk.Label(right_panel, text=self.selected_sentence)
        title1.pack(pady=10)
        self.root.mainloop()

    def upload_file(self, text_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.essay = content
                text_widget.delete('1.0', tk.END)
                text_widget.insert(tk.END, content)

    def analyze_text(self, text_widget):
        results = self.analyzer.process_data(self.essay)
        pattern = r'\d+\.\s+"(.*?)"'

        # Find all matches
        result_sentences = re.findall(pattern, results, re.DOTALL)
        for index, sentence in enumerate(result_sentences):
            start_index = self.essay.find(sentence)
            if start_index != -1:
                if not start_index == 0:
                    end_index = start_index + len(sentence)
                    start_position = text_widget.index(f"1.0+{start_index}c")
                    end_position = text_widget.index(f"1.0+{end_index}c")
                    tag_name = f"highlight_{index}"
                    text_widget.tag_add(tag_name, start_position, end_position)
                    text_widget.tag_config(tag_name, background='yellow', foreground='black')

                    # Bind event to the tag
                    def on_click(event, s=sentence):
                        print(f"Clicked on highlighted text: {s}")
                        self.selected_sentence = s
                        self.root.update()

                    text_widget.tag_bind(tag_name, "<Button-1>", on_click)
            else:
                print("nooooo")
                print("+" + sentence + "+")


if __name__ == "__main__":
    analysis = analyzer.Analyzer()
    ui = UIClass(analysis)
    ui.create_ui()
