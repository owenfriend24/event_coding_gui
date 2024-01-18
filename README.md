# event_coding_gui
Simple Python GUI to segment free recall transcripts into discrete events and categorize those events

### Current Version (v1)
The current version allows users to copy transcribed text into the GUI and then highlight blocks of text and click category buttons to assign words/phrases to specific categories. Current categories are based on the Autobiographical Memory Interview (Kopelman, 1989). When users are finished assigning categories to transcripts, they can save out a csv file with one column for each categorized utterance and one column for its assigned category. The text box is then cleared so that another transcript can be processed.

### Running the GUI
The only dependency required to use this GUI on a Python system is tkinter. Run 'pip install tk' in the terminal to download, but refer to as 'tkinter' in import statements (e.g., 'import tkinter as tk'). Not sure why the pip packaging is slightly different. To open GUI enter 'python event_code_gui.py' into terminal

### Adapting for future work
This GUI is super simple and can be easily adapted for any free recall coding or any work aiming to segment passages of text into smaller components. The main edits you'll need to make are 1. replacing the categories on initialization to your own categories and 2. replacing the categories and colors in the get_category_color function. Color codes are hexadecimal, and if you run out of differentiable colors to highlight text with, this code could be adapted to that the text is colored based on category rather than highilghted. The rest of the code should be commented sufficiently to make changes if you'd like to further adapt the GUI. 
