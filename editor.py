import tkinter as tk

"""

Text editor in python using Tkinter. Follows pymike00 on youtube
https://www.youtube.com/watch?v=7PGFin30c4o&t=230s

"""

class Editor:
    """
    Main class for the text editor.
    """

    def __init__(self, master):
        """
        Initializes the text editor.
        Args:
            master (tkinter instanse): the main window of the application.
        """
        # set the title and initial size
        master.title("Untitled - Editor")
        master.geometry("1200x700")
        self.master = master

        font_specs = ("ubuntu", 18) # sets font family and size

        # initalize the text widget
        self.textarea = tk.Text(master, font=font_specs)
        # allow scroling with scrollbar widget
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        # set up scrolling with mouse
        self.textarea.configure(yscrollcommand=self.scroll.set)
        # set text entry to start at the left side and fill both sides and expand all the way
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # make scrollbar on the right side and fill the entire Y axis
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # configure menubar
        self.menubar = MenuBar(self)


    def set_window_title(self):
        pass

    def new_file(self):
        pass

    def open_file(self):
        pass

    def save(self):
        pass

    def save_as(self):
        pass

    def exit(self):
        self.master.destroy()


class MenuBar:

    def __init__(self, editor):
        font_specs = ("ubuntu", 12) # sets font family and size

        menubar = tk.Menu(editor.master, font=font_specs)
        editor.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="New File", command=editor.new_file)
        file_dropdown.add_command(label="Open File", command=editor.open_file)
        file_dropdown.add_command(label="Save", command=editor.save)
        file_dropdown.add_command(label="Save as", command=editor.save_as)
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit", command=editor.exit)

        menubar.add_cascade(label="File", menu=file_dropdown)




"""
In Python, pydoc as well as unit tests require modules to be importable.
Your code should always check if __name__ == '__main__' before executing
your main program so that the main program is not executed when the module is imported.
"""
if __name__ == "__main__":
    """
    Runs main loop of the program
    """
    master = tk.Tk()
    pt = Editor(master)
    master.mainloop()