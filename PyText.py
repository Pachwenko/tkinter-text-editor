import tkinter as tk
from tkinter import \
    filedialog  # allows navigation between files and folders on the system
from tkinter import messagebox
from typing import List, Tuple

"""

Text editor in python using Tkinter. Follows pymike00 on youtube
https://www.youtube.com/watch?v=7PGFin30c4o&t=230s

"""


class PyText:
    """
    Main class for the text editor.
    """
    file_types: List[Tuple[str, str]]

    def __init__(self, root=tk.Tk()):
        """
        Initializes the text editor.

        Controls the whole editor, should be used to run the program
        and no other methods need to be called under normal circumstance.

        :param root: the instance of TK to use, defaults to
            creating a new instance using tk.Tk()
        """

        # set the title and initial size
        root.geometry("1200x700")
        self.master = root
        self.set_window_title()
        self.filepath = None

        font_specs = ("ubuntu", 18)  # sets font family and size

        # initalize the text widget
        self.textarea = tk.Text(root, font=font_specs)
        # allow scroling with scrollbar widget
        self.scroll = tk.Scrollbar(root, command=self.textarea.yview)
        # set up scrolling with mouse
        self.textarea.configure(yscrollcommand=self.scroll.set)
        # set text entry to start at the left side
        # and fill both sides and expand all the way
        self.textarea.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        # make scrollbar on the right side and fill the entire Y axis
        self.scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # initialize the menubar
        self.menubar = MenuBar(self)

        # initialize the statusbar
        self.statusbar = StatusBar(self)

        # bind shortcuts to our defined methods,
        # but make sure we have a statusbar already initialized first!
        self.bind_shortcuts()



        # all the supported filetypes
        self.file_types = [("All Files", "*.*"),
                           ("Text Files", "*.txt"),
                           ("Python Files", "*.py"),
                           ("Javascript Files", "*.js"),
                           ("HTML Files", "*.html"),
                           ("CSS Files", "*.css"),
                           ("Markdown Documents", "*.md")]

        root.mainloop()

    def set_window_title(self, name=None):
        """
        Sets the window title
        :param name: the name to set the title to, default None
        :return: None
        """
        if name:
            self.master.title(name + " - PyText")
        else:
            self.master.title("Untitled - PyText")

    def new_file(self, *args):
        """
        Creates a new file and sets the window title to Untitled
        :param *args: extra arguments not used
        :return: None
        """
        self.clear_text_area()
        self.filepath = None
        self.set_window_title()

    def open_file(self, *args):
        """
        Opens dialog widget to ask user what file they want to open.
        Does not save the currently opened file first!!

        :param *args: extra arguments not used
        :return: None
        """
        # TODO: Save currently opened file if one is open
        # use filedialog to find the filepath
        # and give it the possible file types we want to open
        self.filepath = filedialog.askopenfilename(
            defaultextension=".txt",
            filetypes=self.file_types
        )
        if self.filepath:
            self.clear_text_area()  # delete everything
            with open(self.filepath, "r") as f:
                self.textarea.insert(1.0,
                                     f.read())  # read the file into the editor
            self.set_window_title(self.filepath)

    def save(self, *args):
        """
        Saves the currently opened file. Updates statusbar.
        If no name has been given previously, prompts user for filename.

        :param *args: extra arguments not used
        :return: None
        """
        if self.filepath:
            try:
                textarea_content = self.textarea.get(1.0, tk.END)
                with open(self.filepath, "w") as f:
                    f.write(textarea_content)
                self.statusbar.update_status(True)
            except Exception as e:
                print(e)
        else:
            self.save_as()

    def save_as(self, *args):
        """
        Opens dialog widget to ask user where and how to save the file.
        Also updated the statusbar

        :param *args: extra arguments not used
        :return: None
        """
        try:
            new_file = filedialog.asksaveasfilename(
                initialfile="Untitled.txt",
                defaultextension=".txt",
                filetypes=self.file_types
            )
            textarea_content = self.textarea.get(1.0, tk.END)
            with open(new_file, "w") as f:
                f.write(textarea_content)
            self.filepath = new_file
            self.set_window_title(self.filepath)
            self.statusbar.update_status(True)
        except Exception as e:
            print(e)

    def clear_text_area(self, begin=1.0, end=tk.END):
        """
        Clears the text area from the specified beginning and end
        Example: Clear entire text area clear_text_area(1.0, tk.END)

        :param begin: the beginning of the buffer to delete from, default is 1.0
        :param end: the end of the buffer we are deleting, defaults to tk.END
        :return: None
        """
        self.textarea.delete(begin, end)

    def bind_shortcuts(self):
        """
        Set up the shortcuts for each keyboard combination.
        Note that the method references are given and not actually called.
        i.e., self.save and not self.save() as that would not work.

        :return: None
        """
        self.textarea.bind("<Control-n>", self.new_file)
        self.textarea.bind("<Control-o>", self.open_file)
        self.textarea.bind("<Control-s>", self.save)
        self.textarea.bind("<Control-S>", self.save_as)
        if self.statusbar:
            self.textarea.bind("<Key>", self.statusbar.update_status)

    def exit(self):
        """
        Destroys and exits the editor.
        :return: None
        """
        # TODO: Save currently open file
        # TODO: or ask the user if they want to save or not
        self.master.destroy()


class StatusBar:
    """
    The statusbar for the text editor. Updates based on user actions
    """

    def __init__(self, parent):
        """
        Initialize the statusbar
        :param parent: the parent window, probably root
        """
        font_specs = ("ubuntu", 12)

        self.status = tk.StringVar() # a string compatible with tk label
        self.status.set("PyText - 0.1 Gutenberg")

        # initialize the statusbar on the bottom left (sw)
        label = tk.Label(parent.textarea, textvariable=self.status,
                         fg="black", bg="lightgrey", anchor="sw",
                         font=font_specs)
        label.pack(side=tk.BOTTOM, fill=tk.BOTH)

    def update_status(self, *args):
        if isinstance(args[0], bool):
            # checks if args[0] is a boolean
            self.status.set("File has been saved.")
        else:
            self.status.set("PyText - 0.1 Gutenberg")



class MenuBar:
    """
    Creates the dropdown menu of the editor.
    """

    def __init__(self, editor):
        """
        Initializes the dropdown menu
        :param editor: the instance of TK to use.
        """
        font_specs = ("ubuntu", 12)  # sets font family and size

        menubar = tk.Menu(editor.master, font=font_specs)
        editor.master.config(menu=menubar)

        file_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        file_dropdown.add_command(label="New File", command=editor.new_file,
                                  accelerator="Ctrl+N")
        file_dropdown.add_command(label="Open File", command=editor.open_file,
                                  accelerator="Ctrl+O")
        file_dropdown.add_command(label="Save", command=editor.save,
                                  accelerator="Ctrl+S")
        file_dropdown.add_command(label="Save as", command=editor.save_as,
                                  accelerator="Ctrl+Shift+S")
        file_dropdown.add_separator()
        file_dropdown.add_command(label="Exit", command=editor.exit)

        about_dropdown = tk.Menu(menubar, font=font_specs, tearoff=0)
        about_dropdown.add_command(label="Release Notes",
                                   command=self.show_release_notes)
        about_dropdown.add_command(label="about",
                                   command=self.show_about_message)

        menubar.add_cascade(label="File", menu=file_dropdown)
        menubar.add_cascade(label="About", menu=about_dropdown)

    def show_about_message(self):
        box_title = "About PyText"
        box_message = "A simple Python Text Editor"
        messagebox.showinfo(box_title, box_message)

    def show_release_notes(self):
        box_title = "Release Notes"
        box_message = "Version 0.1 - Gutenberg\nTutorial by pymike00\nCode by Patrick McCartney"

        messagebox.showinfo(box_title, box_message)


"""
In Python, pydoc as well as unit tests require modules to be importable.
Your code should always check if __name__ == '__main__' before executing
your main program so that the main program
is not executed when the module is imported.
"""
if __name__ == "__main__":
    """
    Runs main loop of the program
    """
    pt = PyText()
