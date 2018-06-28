#!/usr/bin/python
from Tkinter import Tk, Label, Button, Checkbutton, BooleanVar, StringVar, Entry, Text, Menu
import subprocess
import sys

class ColmaUI:

  def getClipboardData(self):
    p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
    retcode = p.wait()
    data = p.stdout.read().decode("utf-8")
    return data

  def setClipboardData(self, data):
    p = subprocess.Popen(['pbcopy'], stdin=subprocess.PIPE)
    p.stdin.write(data)
    p.stdin.close()
    retcode = p.wait()

  def refreshClipboardVar(self, obj):
    obj.set(self.getClipboardData())
    root.update_idletasks()

  def flattenAndJoin(self, source_text, add_spaces, use_quotes, preserve_lines, reverse, unique_only, order_alpha, skip_header):
    # Init character variables
    print "Processing Requested"
    print 'source_text: ', source_text.get()
    print 'add_spaces: ', add_spaces.get()
    print 'use_quotes: ', use_quotes.get()
    print 'preserve_lines: ', preserve_lines.get()
    print 'reverse: ', reverse.get()
    print 'unique_only: ', unique_only.get()
    print 'order_alpha: ', order_alpha.get()
    print 'skip_header: ', skip_header.get()
    output = ''
    space = ' ' if add_spaces.get() else ''
    quote = '\'' if use_quotes.get() else ''
    separator = '\n' if preserve_lines.get() else ','
    split_on = ',' if reverse.get() else '\n'
    separator = '\n' if reverse.get() else separator

    input = source_text.get().split(split_on);
    input = filter(None, input)

    input = list(set(input)) if unique_only.get() else input
    input = sorted(input) if order_alpha.get() else input

    inputlines = len(input)

    headerLineCount = 1 if skip_header.get() else 0

    for i in range(headerLineCount,inputlines):
      # print input[i]
      if i == headerLineCount:
        output = quote + input[i].strip() + quote
      elif input[i] != '':
        output = output + separator + space + quote + input[i].strip() + quote

    return output

  def __init__(self, master):
    # Master Window
    self.master = master
    master.title("colmaUI")

    source_text = StringVar()
    source_text.set(self.getClipboardData())
    output_text = StringVar()
    output_text.set('')

    self.refresh_button = Button(master, text="Paste", command=lambda:source_text.set(self.getClipboardData()), anchor='w')
    self.refresh_button.pack()
    self.refresh_button = Button(master, text="Reset", command=lambda:source_text.set(output_text.get()))
    self.refresh_button.pack()
    self.label = Label(master, textvar=source_text, justify='left', width=10, height=10, relief='groove')
    self.label.pack(expand='yes', fill='both')

    # Spaces between Elements
    add_spaces = BooleanVar()
    add_spaces.set(1)
    self.space_check = Checkbutton(master, text="Add spaces between each value", variable=add_spaces, anchor='w')
    self.space_check.pack()

    # Quoting
    use_quotes = BooleanVar()
    use_quotes.set(0)
    self.quote_check = Checkbutton(master, text="Surround each element with quotes", variable=use_quotes)
    self.quote_check.pack()

    # One line output
    preserve_lines = BooleanVar()
    preserve_lines.set(False)
    self.line_check = Checkbutton(master, text="Don't strip new lines", variable=preserve_lines)
    self.line_check.pack()

    # Split on comma instead of newline
    reverse = BooleanVar()
    reverse.set(0)
    self.rev_check = Checkbutton(master, text="Reverse From CSV to Column", variable=reverse)
    self.rev_check.pack()

    order_alpha = BooleanVar()
    order_alpha.set(0)
    self.order_check = Checkbutton(master, text="Sort alphabetically", variable=order_alpha)
    self.order_check.pack()

    unique_only = BooleanVar()
    unique_only.set(0)
    self.unique_check = Checkbutton(master, text="Unique Values", variable=unique_only)
    self.unique_check.pack()

    skip_header = BooleanVar()
    skip_header.set(0)
    self.header_check = Checkbutton(master, text="Skip Header", variable=skip_header)
    self.header_check.pack()

    self.label = Label(master, textvar=output_text, justify='left', width=10, height=10, relief='groove')
    self.label.pack(expand='yes', fill='both')

    self.go_button = Button(master, text="Process", command=lambda: output_text.set(self.flattenAndJoin(source_text, add_spaces, use_quotes, preserve_lines, reverse, unique_only, order_alpha, skip_header)))
    self.go_button.pack()

    self.copy_button = Button(master, text="Copy", command=lambda: self.setClipboardData(output_text.get()))
    self.copy_button.pack()

    self.close_button = Button(master, text="Quit", command=master.quit)
    self.close_button.pack()


if __name__ == "__main__":
    root = Tk()
    root.minsize(width=280, height=400)
    my_gui = ColmaUI(root)
    root.mainloop()
