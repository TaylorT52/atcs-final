import tkinter as tk
from tkinter import filedialog
from tkinter.scrolledtext import ScrolledText

class UIClass():
    def __init__(self):
        self.root = tk.Tk()
        self.WIDTH = 1500
        self.HEIGHT = 700
        self.PANELWIDTH = 350
        self.essay = ""
    
    def create_ui(self):
        self.root.title("Essay Annihilator")
        self.root.geometry(f"{self.WIDTH}x{self.HEIGHT}")

        # lhs panel for text display
        left_panel = tk.Frame(self.root, bg='white')
        left_panel.pack(side='left', fill='both', expand=True)

        text_area = ScrolledText(left_panel, wrap=tk.WORD, bg="white", font=('Times New Roman', 18), foreground="black")
        text_area.pack(padx=10, pady=10, fill='both', expand=True)

        # rhs panel for controls
        right_panel = tk.Frame(self.root, bg='lightgray', width=self.PANELWIDTH) 
        right_panel.pack(side='right', fill='both', expand=True)

        # upload text files & display their content
        upload_button = tk.Button(right_panel, text='Upload Text File', bg="lightgray", fg="black", highlightbackground='black', font=('Times New Roman', 18), command=lambda: self.upload_file(text_area))
        upload_button.pack(pady=25, padx=20)

        # analyze text
        analyze_button = tk.Button(right_panel, text='Analyze Text', bg="lightgray", fg="black", highlightbackground='black', font=('Times New Roman', 18), command=lambda: self.analyze_text(text_area))
        analyze_button.pack(pady=10, padx=20)

        label_1 = tk.Label(self.root, text ='Highlight Key', bg="lightgray", fg='black', font=('Times New Roman', 18))
        label_1.place(relx = 0.85, rely = 0.35, anchor = 'center')

        label_2 = tk.Label(self.root, text="Hasty Generalization", bg='yellow', fg='black', font=('Times New Roman', 18))
        label_2.place(relx = 0.85, rely = 0.40, anchor = 'center')

        self.root.mainloop()

    def upload_file(self, text_widget):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'r') as file:
                content = file.read()
                self.essay = content
                text_widget.delete('1.0', tk.END) 
                text_widget.insert(tk.END, content) 
                data = content

    def add_highlighter(self):
        text.tag_add("start", "1.11","1.17")
        text.tag_config("start", background= "black", foreground= "white")

    def analyze_text(self, text_widget):
        print("analyze text goes here")
        print(self.essay)

if __name__ == "__main__":
    ui = UIClass()
    ui.create_ui()
