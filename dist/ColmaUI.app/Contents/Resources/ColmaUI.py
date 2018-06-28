#!/usr/bin/python
from Tkinter import Tk, Label, Button, Checkbutton, BooleanVar, StringVar, Entry, Text, Menu, Frame, Radiobutton, Message, OptionMenu, LabelFrame
import ttk
from ttk import Notebook
import subprocess
import sys
import os
import string
from datetime import datetime, time, date

################################################
# TODO
#################
# Code Refactoring Mode:
   # Take all arguments between brackets and egyptize them
   # The inverse of the above

# SQL Value Mode

# Date Generation

# OS Dependant Rendering (Retina consideration)

#################################################
# Settings ##
horizontalSize = 740
verticalSize = 820
fontString = "Hack 9"
#######################

MODES = dict([
  (",", ","),
  (";", ";"),
  ("|", "|"),
  ("~", "~"),
  ("/", "/"),
  ("\\s", " "),
  (".\\s", ". "),
  ("\\n", "\n"),
  ("\\n,", "\n,"),
  ("\\t", "\t"),
  ("", "none")
])

# Retina Display #
if sys.platform == 'darwin':
  horizontalSize = 720
  verticalSize = 840
  fontString = "Hack 12"

class ColmaUI:

  # Get the contents of the clipboard. OS Independent
  def getClipboard(self):
    data = ''
    data = self.master.clipboard_get()
    try:
      data = self.master.clipboard_get()
    except:
      print("Unexpected error:", sys.exc_info()[0])
    return data

  def setClipboard(self, data):
    self.master.clipboard_clear()
    self.master.clipboard_append(data)

  # Find Replace Method
  def findReplace(self, source_text, find_text, replace_text):
    return source_text.replace(find_text, replace_text)

  # Main Delimiter Reorg Code
  def process(self, source_text, src_delimiter, out_delimiter, quote, sort, header, remove_empty, unique, capitalize, prefix, suffix, find, replace):
    output = ''

    src_delimiter = MODES.get(src_delimiter)
    out_delimiter = MODES.get(out_delimiter)

    # Do find replace if entered
    source_text = source_text.replace(find, replace) if (find != '') else source_text

    source_text = source_text.split(src_delimiter) if src_delimiter else source_text

    if header:
      del source_text[0]

    source_text = list(filter(None, source_text)) if remove_empty else source_text
    source_text = list(set(source_text)) if unique else source_text

    source_text = sorted(source_text) if sort else source_text
    source_lines = len(source_text)

    for i in range(0,source_lines):
      nextline = source_text[i].strip()

      # capitalize safely with short or empty strings
      nextline = nextline[0].upper() if capitalize and len(nextline) == 1 else nextline
      nextline = nextline[0].upper()+nextline[1:] if capitalize and len(nextline) > 1 else nextline

      # This could be managed better.
      # add delimiters on each line after the first
      if i == 0:
        output = prefix + quote + nextline + quote + suffix
      elif source_text[i] != '':
        output = output + (out_delimiter if out_delimiter != 'none' else '') + prefix + quote + nextline + quote + suffix

    return output

  def printDate(self, format):
    currentDate = datetime.now()
    day = str(currentDate.day)
    month = str(currentDate.month)
    year = str(currentDate.year)
    hour = str(currentDate.hour)
    minute = str(currentDate.minute)
    second = str(currentDate.second)

    # Do a string replace on the format string
    format = format.replace('Y', year)
    format = format.replace('M', month.zfill(2))
    format = format.replace('D', day.zfill(2))
    format = format.replace('h', hour.zfill(2))
    format = format.replace('m', minute.zfill(2))
    format = format.replace('s', second.zfill(2))

    return format

  def __init__(self, master):
    # Master Window
    self.master = master

    NUMLINES = 32
    BOXWIDTH = 42
    BUTTONWIDTH = 24
    CHECKWIDTH = 24
    BUTTONPAD = 12

    BG_COLOR1 = 'black'

    # Input Box
    BG_COLOR2 = '#301313'

    # Output Box
    BG_COLOR3 = '#131313'

    BG_COLOR4 = '#333333'
    BG_COLOR5 = '#433333'

    # Text
    FG_COLOR1 = 'white'
    FG_COLOR1 = 'grey'

    BD_COLOR1 = '#120000'

    FIELD_WIDTH = 9


    # Delimiter Options
    # Display, characterString
    global MODES;

    DELIMITERS = list(MODES.keys());

    # Date String options
    DATEFORMATS = {
      'YMDhm',
      'YMD_hm',
      'D/M/Y',
      'D/M/Y h:m:s',
      'D/M/Y h:m',
      'Y-M-D',
      'Y-M-D h:m:s',
      'Y-M-D h:m'
    }

    # Initialize the source text.
    source_text_on_load = StringVar()
    source_text_on_load.set(self.getClipboard())
    source_text = StringVar()
    source_text.set(source_text_on_load.get())
    output_text = StringVar()
    output_text.set('')

    src_delimiter = StringVar()
    src_delimiter.set('\n')
    out_delimiter = StringVar()
    out_delimiter.set(',')
    out_quote = StringVar()
    out_quote.set('')

    prefix = StringVar()
    prefix.set('')
    suffix = StringVar()
    suffix.set('')

    find_text = StringVar()
    find_text.set('')
    replace_text = StringVar()
    replace_text.set('')

    capitalize = BooleanVar()
    remove_empty = BooleanVar()
    order_alpha = BooleanVar()
    unique_only = BooleanVar()
    skip_header = BooleanVar()

    capitalize.set(0)
    remove_empty.set(0)
    order_alpha.set(0)
    unique_only.set(0)
    skip_header.set(0)

    date_format = StringVar()
    date_format.set('YMDhm')

##################
# NOTEBOOK 1
################

#################
# TOP
################
    top_frame = Frame(root, bg='', width=36, height=260,pady=3, padx=3)
    top_frame.pack()

    line_numbers = StringVar()
    for i in range(0,NUMLINES):
        line_numbers.set(line_numbers.get() + str(i+1) + '\n')

    # Source Text Box
    source_text_frame = LabelFrame(top_frame, text='Source', fg=FG_COLOR1, bg=BD_COLOR1, width=20, height=400, pady=3, padx=3)
    source_text_frame.grid(row=0, column=1, sticky="nw")
    src_txt_line_numbers = Label(source_text_frame, textvar=line_numbers, fg=FG_COLOR1, bg=BG_COLOR4, anchor='ne', justify='right', width=2, height=NUMLINES, relief='raised')
    src_txt_line_numbers.grid(row=0, column=0)
    src_txt_box = Label(source_text_frame, textvar=source_text, fg=FG_COLOR1, bg=BG_COLOR3, anchor='nw', justify='left', wraplength=320, width=BOXWIDTH, height=NUMLINES, relief='raised')
    src_txt_box.grid(row=0, column=1)

    # Output Text Box
    output_text_frame = LabelFrame(top_frame, text='Output', fg=FG_COLOR1, bg=BD_COLOR1, width=20, height=400, pady=3, padx=3)
    output_text_frame.grid(row=0, column=3, sticky="ne")
    out_txt_box = Label(output_text_frame, textvar=line_numbers, fg=FG_COLOR1, bg=BG_COLOR5, anchor='ne', justify='right', width=2, height=NUMLINES, relief='raised')
    out_txt_box.grid(row=0, column=0)
    out_txt_box = Label(output_text_frame, textvar=output_text, fg=FG_COLOR1, bg=BG_COLOR2, anchor='nw', justify='left', wraplength=320, width=BOXWIDTH, height=NUMLINES, relief='raised')
    out_txt_box.grid(row=0, column=1)


#################
# MIDDLE
################
    # delimiter_frame = LabelFrame(master, fg=FG_COLOR1, bg=BG_COLOR1, pady=10, text='Delimiter Settings')
    # delimiter_frame.pack()

    delimiter_frame = LabelFrame(master, fg=FG_COLOR1, bg=BG_COLOR1, pady=10, text='Delmiter (From -> To)')
    delimiter_frame.pack()

    # MIDDLE LEFT
    src_delimiter_container = Frame(delimiter_frame, bg=BG_COLOR1, padx=5)
    src_delimiter_container.grid(sticky=('n','w','s','e'), row=0, column=0, columnspan=3)

    # src_delimiter_label = Label(src_delimiter_container, text="Src", justify='left', height=1, width=3, anchor='e', relief='groove')
    # src_delimiter_label.grid(row=0, column=0, sticky=('n','w','s','e'))

    # src_delimiter_radio = Frame(src_delimiter_container, relief='groove')
    # src_delimiter_radio.grid(row=0, column=1, sticky=('n','w','s','e'))
    #
    # i = 0
    # for text, mode in MODES:
    #     b = Radiobutton(src_delimiter_radio, text=text, width=8,
    #                     variable=src_delimiter, value=mode, indicatoron=0)
    #     b.grid(row=0, column=i)
    #     i = i+1

    src_delimiter_option = OptionMenu(delimiter_frame, src_delimiter, *DELIMITERS) # Pointer to option array
    src_delimiter_option.grid(row=0, column=0)

    # MIDDLE MIDDLE - Delimiter
    out_delimiter_container = Frame(delimiter_frame, bg=BG_COLOR1, padx=5)
    out_delimiter_container.grid(sticky=('n','w','s','e'), row=1, column=0, columnspan=3)

    # out_delimiter_label = Label(out_delimiter_container, text="Out", justify='center', height=1, width=3, anchor='e', relief='groove')
    # out_delimiter_label.grid(sticky=('n','w','s','e'),row=0, column=0)
    #
    # out_delimiter_radio = Frame(out_delimiter_container, width=240, height=120, relief='groove')
    # out_delimiter_radio.grid(sticky=('n','w','s','e'),row=0, column=1)
    #
    # i = 1
    # for text, mode in MODES:
    #     if mode != 'none':
    #       b = Radiobutton(out_delimiter_radio, text=text, width=8,
    #                       variable=out_delimiter, value=mode, indicatoron=0)
    #       b.grid(row=0, column=i)
    #       i = i+1

    out_delimiter_option = OptionMenu(delimiter_frame, out_delimiter, *DELIMITERS) # Pointer to option array
    out_delimiter_option.grid(row=0, column=1)

    mid_container = Frame(master, bg=BG_COLOR1)
    mid_container.pack()

    textvar_container = LabelFrame(mid_container, fg=FG_COLOR1, bg=BG_COLOR1, pady=10, text='Text Operations')
    textvar_container.grid(row=0, column=0, columnspan=5)

    # MIDDLE BOTTOM - Quote
    out_quote_container = Frame(textvar_container, bg=BG_COLOR1, width=100, height=160, pady=8)
    out_quote_container.grid(row=0, column=0)

    out_quote_label = Label(out_quote_container, text="Quote", justify='center', width=FIELD_WIDTH, height=1, relief='groove')
    out_quote_label.grid(row=0, column=0)

    out_quote_entry = Entry(out_quote_container, textvar=out_quote, justify='center', width=FIELD_WIDTH, relief='groove', bg=FG_COLOR1, fg=BG_COLOR1)
    out_quote_entry.grid(row=1, column=0)

    # MIDDLE BOTTOM - Prefix
    prefix_container = Frame(textvar_container, bg=BG_COLOR1, width=100, height=160, pady=8)
    prefix_container.grid(row=0, column=1)

    prefix_label = Label(prefix_container, text="Prefix", justify='center', width=FIELD_WIDTH, height=1, relief='groove')
    prefix_label.grid(row=0, column=0)

    prefix_entry = Entry(prefix_container, textvar=prefix, justify='center', width=FIELD_WIDTH, relief='groove', bg=FG_COLOR1, fg=BG_COLOR1)
    prefix_entry.grid(row=1, column=0)


    # MIDDLE BOTTOM - Suffix
    suffix_container = Frame(textvar_container, bg=BG_COLOR1, width=100, height=160, pady=8)
    suffix_container.grid(row=0, column=2)

    suffix_label = Label(suffix_container, text="Suffix", justify='center', width=FIELD_WIDTH, height=1, relief='groove')
    suffix_label.grid(row=0, column=0)

    suffix_entry = Entry(suffix_container, textvar=suffix, justify='center', width=FIELD_WIDTH, relief='groove', bg=FG_COLOR1, fg=BG_COLOR1)
    suffix_entry.grid(row=1, column=0)

######################
# FIND REPLACE PANEL #
######################
    find_container = Frame(textvar_container, bg=BG_COLOR1, width=100, height=160, pady=8)
    find_container.grid(row=0, column=3)

    find_label = Label(find_container, text="Replace", justify='left', width=FIELD_WIDTH, height=1, relief='groove')
    find_label.grid(row=0, column=0)

    find_entry = Entry(find_container, textvar=find_text, justify='left', width=FIELD_WIDTH*2, relief='groove', bg=FG_COLOR1, fg=BG_COLOR1)
    find_entry.grid(row=1, column=0)

    replace_container = Frame(textvar_container, bg=BG_COLOR1, width=100, height=160, pady=8)
    replace_container.grid(row=0, column=4)

    replace_label = Label(replace_container, text="With", justify='left', width=FIELD_WIDTH, height=1, relief='groove')
    replace_label.grid(row=0, column=0)

    replace_entry = Entry(replace_container, textvar=replace_text, justify='left', width=FIELD_WIDTH*2, relief='groove', bg=FG_COLOR1, fg=BG_COLOR1)
    replace_entry.grid(row=1, column=0)

# DATE MENU
    date_frame = LabelFrame(mid_container, bg=BG_COLOR1, fg=FG_COLOR1, text='Date', width=650, height=280, pady=3, padx=3, relief='groove')
    date_frame.grid(row=0, column=6)

    date_option = OptionMenu(date_frame, date_format, *DATEFORMATS) # Pointer to option array
    date_option.grid(row=0, column=0)

    date_button = Button(
      date_frame,
      text="Copy",
      command=lambda: self.setClipboard(self.printDate(date_format.get())),
      width=BUTTONWIDTH/2,
      highlightbackground=BG_COLOR1,
    )
    date_button.grid(row=1, column=0)


#################
# BOTTOM
################
    control_frame = Frame(root, bg='', width=650, height=140, pady=3, padx=3, relief='groove')
    control_frame.pack()
#
# # BOTTOM LEFT
    src_control_container = Frame(control_frame, bg=BG_COLOR1, width=200, height=280, padx=BUTTONPAD)
    src_control_container.grid(sticky='w', row=0, column=0)

    # Refresh State to Load
    refresh_button = Button(
      src_control_container,
      text="Refresh To Load State",
      command=lambda:source_text.set(source_text_on_load.get()),
      width=BUTTONWIDTH,
      highlightbackground=BG_COLOR1
    )
    refresh_button.grid(row=0, column=0)

    clipboard_button = Button(
      src_control_container,
      text="Copy from Clipboard",
      command=lambda:source_text.set(self.getClipboard()),
      width=BUTTONWIDTH,
      highlightbackground=BG_COLOR1
    )
    clipboard_button.grid(row=1, column=0)

    pushback_button = Button(
      src_control_container,
      text="Output to Input",
      command=lambda:source_text.set(output_text.get()),
      width=BUTTONWIDTH,
      highlightbackground=BG_COLOR1
    )
    pushback_button.grid(row=2, column=0)

# BOTTOM MIDDLE
    settings_container = Frame(control_frame, bg='grey', width=200, height=280, pady=3, padx=3)
    settings_container.grid(row=0, column=1)

    order_check = Checkbutton(settings_container, text="Alphabeticalize", variable=order_alpha, anchor='w', width=CHECKWIDTH)
    order_check.pack(anchor='w')

    cap_check = Checkbutton(settings_container, text="Capitalize", variable=capitalize, anchor='w', width=CHECKWIDTH)
    cap_check.pack(anchor='w')

    header_check = Checkbutton(settings_container, text="Skip Header", variable=skip_header, anchor='w', width=CHECKWIDTH)
    header_check.pack(anchor='w')

    rem_check = Checkbutton(settings_container, text="Strip Blanks", variable=remove_empty, anchor='w', width=CHECKWIDTH)
    rem_check.pack(anchor='w')

    unique_check = Checkbutton(settings_container, text="Unique Values", variable=unique_only, anchor='w', width=CHECKWIDTH)
    unique_check.pack(anchor='w')

# BOTTOM RIGHT
    out_control_container = Frame(control_frame, bg=BG_COLOR1, width=200, height=280, padx=BUTTONPAD)
    out_control_container.grid(row=0, column=2)

    fr_button = Button(
      out_control_container,
      text="Find/Replace",
      command=lambda: output_text.set(self.findReplace(
        source_text.get(), find_text.get(), replace_text.get()
      )),
      width=BUTTONWIDTH,
      highlightbackground=BG_COLOR1,
    )
    fr_button.pack()

    go_button = Button(
      out_control_container,
      text="Process",
      command=lambda: output_text.set(self.process(
        source_text.get(), src_delimiter.get(), out_delimiter.get(),
        out_quote.get(), order_alpha.get(),
        skip_header.get(), remove_empty.get(), unique_only.get(),
        capitalize.get(), prefix.get(), suffix.get(), find_text.get(), replace_text.get()
      )),
      width=BUTTONWIDTH,
      highlightbackground=BG_COLOR1,
    )
    go_button.pack()

    copy_button = Button(
      out_control_container,
      text="Copy to Clipboard",
      command=lambda: self.setClipboard(output_text.get()),
      width=BUTTONWIDTH,
      highlightbackground=BG_COLOR1
    )
    copy_button.pack()

    close_button = Button(
      out_control_container,
      text="Quit",
      command=master.quit,
      width=BUTTONWIDTH,
      highlightbackground=BG_COLOR1
    )
    close_button.pack()




# END OF CLASS ColmaUI

###############
# Main Method
############
if __name__ == "__main__":
    root = Tk()
    root.title("ColmaUI")
    root.configure(background='black')

    root.geometry('{}x{}'.format(horizontalSize, verticalSize))

    # root.geometry() will return '1x1+0+0' here
    root.update()
    # now root.geometry() returns valid size/placement
    root.minsize(root.winfo_width(), root.winfo_height())

    root.option_add("*Font", fontString)
    my_gui = ColmaUI(root)

    root.mainloop()
