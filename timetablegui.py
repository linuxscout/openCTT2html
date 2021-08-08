#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  test1.py
#  
#  Copyright 2019 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
# 
import os
import sys
#~ import arabic_reshaper
#~ from bidi.algorithm import get_display
import pyarabic.unshape

from tkinter import Tk, Label, Button, Entry, IntVar, END, W, E, Text
from tkinter import OptionMenu, StringVar, Menu
from tkinter import messagebox as tkMessageBox
from tkhtmlview import HTMLLabel, HTMLText, HTMLScrolledText
# import filedialog module
from tkinter import filedialog

#~ from convert import *
# ~ import adawat.adawat
import timetable.tm as tm

def donothing():
   tkMessageBox.showinfo("Alert", "Not yet implemented")
class myToolbox:

    def __init__(self, master):
        # ~ self.adw = adawat.adawat.Adawat()
        # opend file
        self.filename = "";
        # parser 
        self.parser = None
        
        self.master = master
        master.title(u"أدوات لاتخ Adawat Latex")
        myfont = os.path.join(sys.path[0],"resources/fonts/AmiriTypewriter-Regular.ttf")

        self.total = 0
        self.entered_number = 0
        # make menu
        self.makemenu()
        self.output_label = Label(master, text="Output")
        self.shape_label = Label(master, text="Shape")

        self.label = Label(master, text="Input:")
        self.label_actions = Label(master, text="Action:")
        self.label_config = Label(master, text="Config:")

        #~ vcmd = master.register(self.validate) # we have to wrap the command
        #self.entry = Text(master, height=15, width=70, font=myfont)
        
        # ~ self.output = Text(master, height=15, width=70, font=myfont)
        self.output = HTMLScrolledText(master, height=30, width=70, font=myfont)
        
        # ~ sampletext = u"""Greating\tالسلام عليكم ورحمة الله وبركاته
# ~ Welcome\tمرحبا\tBien venue
# ~ Welcome\tأهلا ووسهلا"""
        # ~ self.entry.insert("1.0", self.bidi(sampletext))
        #~ self.nshape = Entry(master, validate="key")
        #~ self.nshape.insert(END,2)
        #~ self.entry = Entry(master, validate="key", validatecommand=(vcmd, '%P'))

        self.tab_button = Button(master, text="Free Rooms", command=lambda: self.update("freerooms"))
        self.lang_button = Button(master, text="Available Teachers", command=lambda: self.update("teachers"))
        self.trans_button = Button(master, text="TimeTable", command=lambda: self.update("timetables"))
        self.reshape_button = Button(master, text="Reshape", command=lambda: self.update("reshape"))
        self.itemize_button = Button(master, text="Itemize", command=lambda: self.update("itemize"))
        self.inverse_button = Button(master, text="Affectation", command=lambda: self.update("affectation"))
        self.tokenize_button = Button(master, text="Charges", command=lambda: self.update("charges"))
        self.list_button = Button(master, text="Python list", command=lambda: self.update("pythonlist"))
        self.tabbing_button = Button(master, text="Tabbing", command=lambda: self.update("tabbing"))
        self.submit_button = Button(master, text="Submit", bg="green", fg="white",command=lambda: self.update("submit"))
        self.reset_button = Button(master, text="Reset", command=lambda: self.update("reset"))
        self.copy_button = Button(master, text="Copy", command=lambda: self.update("copy"))
        self.recopy_button = Button(master, text="Recopy", command=lambda: self.update("recopy"))


        #format options 
        OPTIONS_FORMAT = ["all", "tp", "salle"]
        self.rooms_opt = StringVar()
        self.rooms_opt.set(OPTIONS_FORMAT[0]) 
        self.rooms_options = OptionMenu(master, self.rooms_opt, *OPTIONS_FORMAT)
        #language options 
        OPTIONS = ["all", "vac", "tp", "cours", "details"]
        self.teacher_opt = StringVar()
        self.teacher_opt.set(OPTIONS[0]) 
        self.teacher_options = OptionMenu(master, self.teacher_opt, *OPTIONS)
        
        # shape options
        OPTIONS_SHAPE = [1,2,3,4,5,6,7,8,9]
        self.shape_opt = IntVar()
        self.shape_opt.set(OPTIONS_SHAPE[2]) 
        self.shape_options = OptionMenu(master, self.shape_opt, *OPTIONS_SHAPE)
        # transliterate 
        OPTIONS_TRANS = ["groups", "teachers", "rooms"]
        self.trans_opt = StringVar()
        self.trans_opt.set(OPTIONS_TRANS[0]) 
        self.trans_options = OptionMenu(master, self.trans_opt, *OPTIONS_TRANS)
        # itemize options
        OPTIONS_ITEM = ["itemize","enumerate"]
        self.itemize_opt = StringVar()
        self.itemize_opt.set(OPTIONS_ITEM[0]) 
        self.itemize_options = OptionMenu(master, self.itemize_opt, *OPTIONS_ITEM)
        # separator options
        OPTIONS_SEP= ["tab", "space", ";",",", "\\t"]
        self.separator_opt = StringVar()
        self.separator_opt.set(OPTIONS_SEP[0]) 
        self.separator_options = OptionMenu(master, self.separator_opt, *OPTIONS_SEP)
        # Actions options
        OPTIONS_ACTION= ["lang",
         "tabulize",
         "inverse",
         "tokenize",
         "tabbing",
         "pythonlist",
         "reshape",
         "trans",
         "itemize",]
        self.action_opt = StringVar()
        self.action_opt.set(OPTIONS_ACTION[0]) 
        self.action_options = OptionMenu(master, self.action_opt, *OPTIONS_ACTION)
        
        
        
        # LAYOUT
        #0
        self.label.grid(row=0, column=0, sticky=W)
        self.label_actions.grid(row=0, column=3, sticky=W)
        self.label_config.grid(row=0, column=4, sticky=W)
        #1
        self.output.grid(row=1, column=0, rowspan=6, columnspan=3, sticky=W+E)

        # ~ self.entry.grid(row=1, column=0, rowspan=6, columnspan=3, sticky=W+E)
        #2 
        self.tab_button.grid(row=2, column=3, sticky=W+E)
        self.rooms_options.grid(row=2, column=4, sticky=W+E)

        #3
        self.lang_button.grid(row=3, column=3, sticky=W+E)
        self.teacher_options.grid(row=3, column=4, sticky=W+E)

        #4 
        self.trans_button.grid(row=4, column=3, sticky=W+E)
        self.trans_options.grid(row=4, column=4, sticky=W+E)        
        #5 
        self.reshape_button.grid(row=5, column=3, sticky=W+E)
        self.shape_options.grid(row=5, column=4, sticky=W+E)        
        #6 
        self.itemize_button.grid(row=6, column=3, sticky=W+E)
        self.itemize_options.grid(row=6, column=4, sticky=W+E)
        #7 Output label
        self.output_label.grid(row=7, column=0, columnspan=1, sticky=W)
        self.submit_button.grid(row=7, column=1, sticky=E)
        self.action_options.grid(row=7, column=2, sticky=W+E)        
        self.tabbing_button.grid(row=7, column=3, sticky=W+E)
        self.separator_options.grid(row=7, column=4, sticky=W+E)
        # 8 
        self.inverse_button.grid(row=8, column=3, sticky=W+E)
        self.tokenize_button.grid(row=8, column=4, sticky=W+E)
        # ~ self.output.grid(row=8, column=0, rowspan=6, columnspan=3, sticky=W+E)
        
        # 9 
        self.list_button.grid(row=9, column=4, sticky=W+E)

        #10
        self.copy_button.grid(row=10, column=3, columnspan=2, sticky=W+E)
        self.recopy_button.grid(row=11, column=3,columnspan=2, sticky=W+E)
        self.reset_button.grid(row=12, column=3, columnspan=2, sticky=W+E)
        #5
    def makemenu(self,):
        menubar = Menu(self.master)
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="New", command=donothing)
        filemenu.add_command(label="Open", command=self.browseFiles)
        filemenu.add_command(label="Save", command=donothing)
        filemenu.add_command(label="Save as...", command=donothing)
        filemenu.add_command(label="Close", command=donothing)

        filemenu.add_separator()

        filemenu.add_command(label="Exit", command=self.master.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=donothing)

        editmenu.add_separator()

        editmenu.add_command(label="Cut", command=donothing)
        editmenu.add_command(label="Copy", command=lambda: self.update("copy"))
        editmenu.add_command(label="ReCopy", command=lambda: self.update("recopy"))
        editmenu.add_command(label="Paste", command=donothing)
        editmenu.add_command(label="Delete", command=lambda: self.update("reset"))
        editmenu.add_command(label="Select All", command=donothing)

        menubar.add_cascade(label="Edit", menu=editmenu)
        
        # latex menu
        latexmenu = Menu(menubar, tearoff=0)
        latexmenu.add_command(label="Tabulize", command=lambda: self.update("tabulize"))
        latexmenu.add_command(label="Language segmentation", command=lambda: self.update("lang"))
        latexmenu.add_command(label="Itemize", command=lambda: self.update("itemize"))
        latexmenu.add_command(label="Tabbing", command=lambda: self.update("tabbing"))
        menubar.add_cascade(label="Latex", menu=latexmenu)
        
        # arabic
        arabicmenu = Menu(menubar, tearoff=0)
        arabicmenu.add_command(label="Transliterate", command=lambda: self.update("trans"))
        arabicmenu.add_command(label="Language segmentation", command=lambda: self.update("lang"))
        arabicmenu.add_command(label="Unshape", command=lambda: self.update("reshape"))
        menubar.add_cascade(label="Arabic", menu=arabicmenu)
        
        # tools
        toolsmenu = Menu(menubar, tearoff=0)
        toolsmenu.add_command(label="CSV to Python list", command=lambda: self.update("pythonlist"))
        toolsmenu.add_command(label="Tokenize", command=lambda: self.update("tokenize"))
        toolsmenu.add_command(label="Tabulize Markdown", command=lambda: self.update("tabulize"))
        menubar.add_cascade(label="Tools", menu=toolsmenu)
        
        helpmenu = Menu(menubar, tearoff=0)
        helpmenu.add_command(label="Help Index", command=lambda: self.update("help"))
        helpmenu.add_command(label="About...", command=lambda: self.update("about"))
        menubar.add_cascade(label="Help", menu=helpmenu)

        self.master.config(menu=menubar)
    # Function for opening the
    # file explorer window
    def browseFiles(self, ):
        self.filename = filedialog.askopenfilename(initialdir = "¬",
                                              title = "Select a File",
                                              filetypes = (("Text files",
                                                            "*.oct*"),
                                                           ("all files",
                                                            "*.*")))
          
        # Change label contents
        # ~ label_file_explorer.configure(text="File Opened: "+filename)
        #~ @staticmethod
        print("filename :", self.filename)
        self.parser = tm.html_displayer(self.filename)
        # ~ result = parser.display_html()
        # ~ self.output.set_html(result)
    def bidi(self, text):
        return text
        #~ reshaped_text  = self.adw.delimite_language_bidi(text, arabic_reshaper.reshape)
        #~ reshaped_text = arabic_reshaper.reshape(text)
        #~ bidi_text = get_display(reshaped_text)
        #~ return bidi_text
    #~ @staticmethod
    def unbidi(self, text):
        return text
        #~ unshaped_text = pyarabic.unshape.unshaping_text(text)
        #~ unshaped_text  = self.adw.delimite_language_bidi(text, pyarabic.unshape.unshaping_text)
        
        #~ bidi_text = get_display(reshaped_text)
        #~ return unshaped_text
    def get_separator(self,):
        sep = self.separator_opt.get()
        if sep =="tab":
            return "\t"
        elif sep =="space":
            return " "
        else:
            return sep
    def help(self):
       tkMessageBox.showinfo("Help", "Not yet implemented")            
    def about(self):
       tkMessageBox.showinfo("Help", self.bidi( u"أدوات لاتخ\n**Adawat Latex**\n developed by Taha Zerrouki") )           
    def update(self, method):
        """
        
        """
        if not self.parser:
            tkMessageBox.showinfo("Info", "You should select a timetable file") 
            return False
        display_format = self.rooms_opt.get()
        if method == "help":
            self.help()
            return True
        if method == "about":
            self.about()
            return True
        if method == "reset":
            self.output.delete("1.0", END)
            # ~ self.entry.delete("1.0", END)
            return True
        if method == "recopy":
            result = self.output.get("1.0",END)
            # ~ self.entry.delete("1.0", END)
            # ~ self.entry.insert("1.0", result)
            return True
        if method == "copy":
            value = self.output.get("1.0",END)
            self.master.clipboard_clear()
            self.master.clipboard_append(self.unbidi(value))
            return True
        if method == "submit":
            command = self.action_opt.get()
            #~ print(command)
        else:
            command = method
        # ~ value = self.entry.get("1.0",END)
        #value = self.unbidi(value)

        if command == "default":
            result = ""
        elif command == "freerooms":
            sep = self.get_separator()
            room_type = self.rooms_opt.get()
            if room_type and room_type!="all":
                command +="_"+room_type
            result = self.parser.action(command)          
        elif command == "teachers":
            sep = self.get_separator()
            command = "availableteachers"
            teacher_type = self.teacher_opt.get()
            if teacher_type and teacher_type!="all":
                command +="_"+teacher_type
            result = self.parser.action(command)          
        elif command == "timetables":
            sep = self.get_separator()
            slot_type = self.trans_opt.get()
            if slot_type and slot_type!="all":
                command +="_"+slot_type
            result = self.parser.action(command)          
        elif command == "affectation":
            result = self.parser.action(command)          
        elif command == "charges":
            result = self.parser.action(command)          
        else: # reset
            donothing()
            result = value
        self.output.delete("1.0", END)
        # ~ self.output.insert("1.0", self.bidi(result))
        self.output.set_html(result)
    



def main(args):
    root = Tk()
    my_gui = myToolbox(root)
    root.mainloop()
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
