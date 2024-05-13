import tkinter as tk
from tkinter import Text, Button, filedialog, messagebox
import csv

class TextCategorizerApp:
    def __init__(self, root):
        self.root = root
        
        # name GUI
        self.root.title("Transcript Event Coding GUI v1")
        
        # add instructions text to top of GUI
        instruction_title = tk.Label(self.root, text="INSTRUCTIONS:")
        instruction_title.pack(pady=5, padx = 5, anchor="w", side="top", fill="x") 
        instruction_label = tk.Label(self.root, text="Copy transcribed text into the box below. Highlight words or phrases and click a category button to assign to that category.\nCategories are mutually exclusive. To change a categorized word/phrase to another category, highlight the word/phrase and then click the new category.\nTo remove a category label from a word/phrase, highlight the word/phrase and click \'Clear\'. \nWhen finished, click \'Save\' to output csv file with all word/phrases and their corresponding category codes. The input box will then clear and can be used again.", justify="left")
        # \nTo denote temporally nested events, use curly brackets around relevant words/phrases (e.g. \'{I get ready, so I brush my teeth and wash my face}\').
        instruction_label.pack(pady=5, padx = 1, anchor="w", side="top", fill="x") 
        
        # create text box for transcribed recall to be pasted into
        self.text_area = Text(self.root, wrap="word", height=40, width=110,undo = True)
        self.text_area.pack(padx=10, pady=10, side="left")

        # categories - make sure name's align with colors assigned below in get_category_color
        self.categories = ["Event", "Place", "Location Change - Same Room", "Location Change - Different Room", "Location Change - Different Location", 
                           "Time", "Sequencing Terms", "Perceptual", "Emotion/Thought", "Repetitions"]
        
        # create category buttons
        category_frame = tk.Frame(self.root)
        category_frame.pack(side="left", padx=5)

        self.category_buttons = []
        for category in self.categories:
            color = self.get_category_color(category)
            btn = Button(category_frame, text=category, command=lambda cat=category: self.assign_category(cat), borderwidth=3, relief="solid", bg=color, highlightbackground=color)
            btn.pack(anchor="w", padx=5)
            self.category_buttons.append(btn)
    
        # add button to clear category assignment
        button_frame = tk.Frame(self.root)
        button_frame.pack(side="left", padx=5)
        clear_btn = Button(button_frame, text="Clear", command=self.clear_category)
        clear_btn.pack(side = "left", pady=10)
        
        # add button to save file as csv
        submit_btn = Button(self.root, text="SAVE", command=self.save_to_csv)
        submit_btn.pack(side = "top", padx=1)

        self.category_assignments = {}

    # assigns selected word/phrase to category
    def assign_category(self, category):
        selected_indices = self.text_area.tag_ranges(tk.SEL)
        if selected_indices:
            start, end = selected_indices
            selected_text = self.text_area.get(start, end)

            existing_category = self.category_assignments.get(selected_text)
            if existing_category:
                self.text_area.tag_remove(existing_category, start, end)

            self.category_assignments[selected_text] = category
            self.text_area.tag_add(category, start, end)
            self.text_area.tag_config(category, background=self.get_category_color(category))

    # clears category from word/phrase so that there is no label
    def clear_category(self):
        selected_indices = self.text_area.tag_ranges(tk.SEL)
        if selected_indices:
            start, end = selected_indices
            selected_text = self.text_area.get(start, end)

            existing_category = self.category_assignments.get(selected_text)
            if existing_category:
                self.text_area.tag_remove(existing_category, start, end)
                del self.category_assignments[selected_text]
            else: 
                messagebox.showerror("Error clearing tag", "An existing tag was not found for the selected text. Make sure you've selected all the text for this tag (including whitespace) and try again. ")


    # Assign unique hex colors for each category; aim to use pretty light colors so you can still read the text when it's highlighted. For more categories, can also add colors to actual text rather than highlighting
    def get_category_color(self, category):
        colors = {"Event": "#f6fa82", "Place": "#b7ff87", "Location Change - Same Room": "#ff8787", "Location Change - Different Room":"#ffb187",
                  "Location Change - Different Location":"#ffd98c", "Time": "#bdd2ff", "Sequencing Terms":"#d7b3ff", "Perceptual":"#ff00b3", "Emotion/Thought":"#bdbdbd", "Repetitions":"#ff0000"}
        return colors.get(category, "#FFFFFF")  # Default to white if category not found
    
    # save file to csv, with one column for selected text, and one column for corresponding category label
    def save_to_csv(self):
        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if filename:
            with open(filename, "w") as file:
                wr = csv.writer(file)
                wr.writerow(['Word/Phrase','Category'])
                for word, category in self.category_assignments.items():
                    wr.writerow([str(word),str(category)])

                # after saving out text with categories, iterate through entire text to save each string within curly brackets as a separate entry
                text_content = self.text_area.get("1.0", tk.END)
                nested_texts = self.extract_nested_texts(text_content)
                for nested_text in nested_texts:
                    wr.writerow([str(nested_text),'nested'])
            file.close()
            messagebox.showinfo("Success", "CSV file saved successfully!")
            
            # clears text box for next transcript so that GUI can stay open/doesn't have to be re-loaded for each transcript
            self.clear_text_area()

    def extract_nested_texts(self, text):
        nested_texts = []
        start_index = text.find('{')
        while start_index != -1:
            end_index = text.find('}', start_index)
            if end_index != -1:
                nested_texts.append(text[start_index + 1:end_index].strip())
                start_index = text.find('{', end_index + 1)
            else:
                break
        return nested_texts
    
    # 
    def clear_text_area(self):
        self.text_area.delete("1.0", tk.END)
        self.category_assignments = {}


if __name__ == "__main__":
    root = tk.Tk()
    app = TextCategorizerApp(root)
    root.mainloop()
