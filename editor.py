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

        # initalize the text widget
        self.textarea = tk.Text(master)
        # allow scroling with scrollbar widget
        self.scroll = tk.Scrollbar(master, command=self.textarea.yview)
        # set up scrolling with mouse
        self.textarea.configure(yscrollcommand=self.scroll.set)


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