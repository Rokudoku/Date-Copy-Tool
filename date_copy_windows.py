#!/usr/bin/env python3
"""
=== Date Copy Tool - Windows Version ===
A tool that copies a specified date to clipboard so that it can be pasted. 

By pressing the 'Today' button or using its hotkey, the current date is 
copied to  clipboard so it may be pasted. This is a similar case with the 
'Yesterday' and 'Tomorrow' buttons.

The format is: <date number> <abbreviated month> <4 digit year>
        e.g. 23 Dec 2016

===========================
By Jerome Probst 
December 2016/January 2017
===========================

===Notable changes from osx version===
'Date' is not a simple commandline tool. Need to use datetime module.
Slightly different ttk settings.
Lots of changes to do with menubar.
"""

import tkinter as tk
from tkinter import ttk
import sys
from datetime import date, timedelta

###Button size constants
SMALL = 50
MEDIUM = 65
LARGE = 80


class MainApp(tk.Frame):
    """
    The parent window.
    Interacts with other sections as classes to make things cleaner and 
    easier to manage if doing more than just the date buttons.
    """

    def __init__(self, parent):
        """
        Sets up self as the mainframe under root and manages all the
        subframes and menu.
        """

        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.dates = Dates(self)
        self.dates.pack()

        self.menubar = Menubar(self)

        self.grid(row=0, column=0, sticky="nsew")


class Dates(tk.Frame):
    """ 
    "Yesterday", "Today" and "Tomorrow" buttons assigned to (1, 2, 3) 
    that copy their respective dates to the clipboard.
    """
    
    def __init__(self, parent):
        """Sets up self as the frame 'Dates'"""

        ttk.Frame.__init__(self, parent)
        self.parent = parent

        self.create_buttons()
        self.set_keybinds()

    def create_buttons(self):
        """
        Creates the "Yesterday", "Today" and "Tomorrow" buttons.
        Default size is medium.
        """

        self.s = ttk.Style()

        self.s.configure("date.TButton", padding=35, width=14)

        self.yesterday_btn = ttk.Button(self, text="Yesterday (1)", 
                        style="date.TButton", 
                        command=lambda: self.copy_date(1))

        self.today_btn = ttk.Button(self, text="Today (2)",
                        style="date.TButton", 
                        command=lambda: self.copy_date(2))

        self.tomorrow_btn = ttk.Button(self, text="Tomorrow (3)",
                        style="date.TButton", 
                        command=lambda: self.copy_date(3))

        self.yesterday_btn.configure(padding=MEDIUM)
        self.today_btn.configure(padding=MEDIUM)
        self.tomorrow_btn.configure(padding=MEDIUM)

        self.yesterday_btn.pack()
        self.today_btn.pack()
        self.tomorrow_btn.pack()

    def set_keybinds(self):
        """
        Sets up the buttons to correspond to 1,2,3. Gets passed the button
        number so copy_date knows what to do.
        """
        
        # Note: seems keybinds must be done at root (self.parent.parent)
        self.parent.parent.bind("1", lambda x: self.copy_date(1))
        self.parent.parent.bind("2", lambda x: self.copy_date(2))
        self.parent.parent.bind("3", lambda x: self.copy_date(3))

    def copy_date(self, option):
        """
        Clears clipboard and depending on option, gives the correct date.
        Uses the inbuilt datetime module.
        (Learned how to do this after doing the bash command option in the osx
        version).
        Also sets focus on the associated button so user knows what they
        pressed.
        """
        
        self.parent.clipboard_clear()
        
        self.date = date.today()

        if option == 1:
            self.yesterday_btn.focus()
            self.date -= timedelta(days=1)
        elif option == 2:
            self.today_btn.focus()
        elif option == 3:
            self.tomorrow_btn.focus()
            self.date += timedelta(days=1)
        else:
            sys.stderr.write('copy_date was called with an invalid arg')
            sys.exit(1)
        
        self.output = self.date.strftime('%d %b %Y')

        if self.parent.menubar.trailing_check.get():
            self.output += ' '

        if self.parent.menubar.leading_check.get():
            self.output = ' ' + self.output

        self.parent.clipboard_append(self.output)


class Menubar(tk.Menu):
    """
    The menubar. Each window can have a menubar attached to it by adjusting it's
    "menu" config option. In this case we are working off of root.
    """

    def __init__(self, parent):
        """
        Uses the __init__ method of Menu to make self a Menu.
        Its parent is the mainframe so it can easily communicate with the
        mainframe attributes and change things such as button size.
        We need to make sure to work with root though (parent of mainframe) for
        making the menu a part of the root window.
        """
        
        self.parent = parent      #remember that this is the mainframe
        self.root = parent.parent
        
        tk.Menu.__init__(self, self.root)
        
        #removes dotted line tearoff option for all the menus
        self.root.option_add('*tearOff', tk.FALSE)

        self.file_menu()
        self.options_menu()
        self.help_menu()

        self.root.config(menu=self)

    def file_menu(self):
        """
        The 'File' menubar.
        Contains 'About' and 'Quit' with a seperator in between.
        """

        self.filemenu = tk.Menu(self)
        self.add_cascade(menu=self.filemenu, label='File')

        self.filemenu.add_command(label='About', command=self.about_window)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Quit', command=self.close_window)

    def about_window(self):
        """
        A new window that gives information about this program.
        """
        
        self.aboutwindow = tk.Toplevel(self.parent)
        self.aboutwindow.title('About Date Copy Tool')
        self.aboutwindow.geometry('300x200' + self.root_coords())
        self.aboutwindow.resizable(tk.FALSE, tk.FALSE)

        self.abouttext = ttk.Label(self.aboutwindow, text='Why hello there')
        self.abouttext.pack()

    def root_coords(self):
        """
        Returns the x/y coordinates of the root window. (as +x+y)
        Used to find out where to place other toplevel windows.
        Don't want to be placed EXACTLY on top, so there is a bit extra.
        """
        
        EXTRA = 30
        
        #.geometry() gets format of heightxwidth+x+y
        coords = self.root.geometry().split('+')
        x = int(coords[1]) + EXTRA
        y = int(coords[2]) + EXTRA
        result = '+' + str(x) + '+' + str(y)
        return result
    
    def close_window(self):
        """Closes the program by destryoing root window."""
        
        self.root.destroy()

    def options_menu(self):
        """
        The 'Options' menubar.
        Contains the 'Size' submenu which determines size of the buttons.
        """
        
        self.optionsmenu = tk.Menu(self)
        self.add_cascade(menu=self.optionsmenu, label='Options')

        self.size = self.size_submenu()
        self.spacing = self.spacing_submenu()

    def size_submenu(self):
        """
        Submenu inside 'Options'. Contains 'Small', 'Medium' and 'Large'.
        These options change the size of the buttons.
        The default is 'Medium'
        """

        self.sizemenu = tk.Menu(self.optionsmenu)
        self.optionsmenu.add_cascade(menu=self.sizemenu, label='Size')

        self.button_size = tk.StringVar()
        self.sizemenu.add_radiobutton(label='Small', 
                                command=lambda:self.change_button_size(SMALL),
                                variable=self.button_size, value='Small')
        self.sizemenu.add_radiobutton(label='Medium', 
                                command=lambda:self.change_button_size(MEDIUM),
                                variable=self.button_size, value='Medium')
        self.sizemenu.add_radiobutton(label='Large', 
                                command=lambda:self.change_button_size(LARGE),
                                variable=self.button_size, value='Large')
        self.button_size.set('Medium')

    def change_button_size(self, size):
        """
        Changes the button size by accessing the dates created in mainframe
        """
        
        self.parent.dates.yesterday_btn.configure(padding=size)
        self.parent.dates.today_btn.configure(padding=size)
        self.parent.dates.tomorrow_btn.configure(padding=size)

    def spacing_submenu(self):
        """
        Submenu inside 'Options'. Allows for trailing or leading space in
        the date that is copied to clipboard. They are either on or off.
        Default is both off.
        """
        
        self.spacingmenu = tk.Menu(self.optionsmenu)
        self.optionsmenu.add_cascade(menu=self.spacingmenu, label='Spacing')

        self.leading_check = tk.BooleanVar()
        self.spacingmenu.add_checkbutton(label='Leading Space', 
                                    variable=self.leading_check,
                                    onvalue=True, offvalue=False)

        self.trailing_check = tk.BooleanVar()
        self.spacingmenu.add_checkbutton(label='Trailing Space',
                                    variable=self.trailing_check,
                                    onvalue=True, offvalue=False)

        ### These Bool values are used when creating the actual output.
        ### (Dates.copy_date)

    def help_menu(self):
        """
        The 'Help' menubar. Contains 'Instructions'.
        """
        
        self.helpmenu = tk.Menu(self)
        self.add_cascade(menu=self.helpmenu, label='Help')

        self.helpmenu.add_command(label='Instructions')

root = tk.Tk()

root.title("Date Copy Tool")

root.rowconfigure(0, weight=1)
root.columnconfigure(0, weight=1)

app = MainApp(root)

root.mainloop()
