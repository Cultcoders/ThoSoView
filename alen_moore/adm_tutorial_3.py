"""
    Jetzt geht es mit Widgets weiter also Nr. 3
    Wird sicher einiges an Umbau gemacht!
"""

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as tkmb
from tkinter import simpledialog as tksd
from tkinter import filedialog as tkfd
from pathlib import Path
from datetime import datetime

# create root
root = tk.Tk()
font_size = tk.IntVar(value=10)
# configure root
root.title('My Diary TTK')
root.geometry('800x600+300+300')
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.configure(bg='#888')

style = ttk.Style()
# style.configure('TLabel', font='Arial 12 bold')
# style.configure('TCheckbutton', font='Arial 14 bold', background='LightSalmon')
# # style.configure('TRadiobutton', font="Arial 14 bold", background='LightSteelBlue')
# style.configure('TLabelframe.Label', font='Arial 16 bold', background='PaleGreen')
# style.configure('Status.TLabel', font='Arial 13', background='PaleGreen')
# # dynamic style
# style.map(
#     'TRadiobutton',
#     font=[('selected', 'Arial 16')]
# )
# style.map(
#     'TCheckbutton',
#     background=[
#         ('selected', 'pink'),
#         ('active', 'red'),
#         ('disabled', 'green')
#     ]
# )
theme_var = tk.StringVar()

notebook = ttk.Notebook(root)
notebook.grid(sticky='nesw', padx=5, pady=5)
notebook.enable_traversal()

# sub-frame for form
form_frame = ttk.Frame(notebook)
# form_frame.grid(sticky=tk.N+tk.E+tk.S+tk.W, padx=3, pady=3)
form_frame.columnconfigure(0, weight=1)
form_frame.rowconfigure(5, weight=1)
notebook.add(form_frame, text='Diary Entry', underline=0)    # underline = id char from text=

# dummy
# dummy_frame = ttk.Frame(notebook)
# notebook.add(dummy_frame, text='Dummy Entry', underline=1)    # underline = id char from text=

# subject
subj_frame = ttk.Frame(form_frame)
subj_frame.columnconfigure(1, weight=1)
subject_var = tk.StringVar()
ttk.Label(
    subj_frame,
    text='Subject: '
).grid(sticky='we', padx=5, pady=5)
ttk.Entry(
    subj_frame,
    textvariable=subject_var
).grid(row=0, column=1, sticky=tk.E + tk.W)
subj_frame.grid(sticky='ew')

# category
cat_frame = ttk.Frame(form_frame)
cat_frame.columnconfigure(1, weight=1)
cat_var = tk.StringVar()
categories = ['Work', 'Hobbies', 'Health', 'Bills']
ttk.Label(
    cat_frame,
    text='Category: '
).grid(sticky=tk.E + tk.W, padx=5, pady=5)
ttk.Combobox(
    cat_frame,
    textvariable=cat_var,
    values=categories
).grid(row=0, column=1, sticky=tk.E + tk.W, padx=5, pady=5)
cat_frame.grid(sticky='ew')

# Private
private_var = tk.BooleanVar(value=False)
ttk.Checkbutton(
    form_frame,
    variable=private_var,
    text='Private? '
).grid(row=2, ipadx=2, ipady=2, sticky=tk.W)

# Datestamp
datestamp_var = tk.StringVar(value='none')
datestamp_frame = ttk.Frame(form_frame)
for value in ('None', 'Date', 'Date+Time'):
    ttk.Radiobutton(
        datestamp_frame,
        text=value,
        value=value,
        variable=datestamp_var
    ).pack(side=tk.LEFT)
datestamp_frame.grid(row=2, sticky='e', padx=3, pady=3)

# seperator
# ttk.Separator(form_frame, orient=tk.HORIZONTAL).grid(sticky='ew')

# message
message_frame = ttk.LabelFrame(form_frame, text='Message')
message_frame.columnconfigure(0, weight=1)
message_frame.rowconfigure(0, weight=1)
message_inp = tk.Text(message_frame, fg='navy', bg='PapayaWhip')
message_inp.grid(sticky='nesw')

scrollbar = ttk.Scrollbar(message_frame)
scrollbar.grid(row=0, column=1, sticky='nes')
message_frame.grid(sticky='nesw')
scrollbar.configure(command=message_inp.yview)
message_inp.configure(yscrollcommand=scrollbar.set)

# save button
save_btn = ttk.Button(
    form_frame,
    text='Save'
)
save_btn.grid(sticky=tk.E + tk.W)

# open button
# open_btn = tk.Button(
#     root,
#     text='Open'
# )
# open_btn.grid(sticky=tk.W + tk.E, ipadx=3, ipady=3)

# status bar
#    style='Status.TLabel' - necessary for status bar label style
status_var = tk.StringVar()
ttk.Label(
    form_frame,
    textvariable=status_var     # insert here style option
).grid(row=100, sticky=tk.W + tk.E + tk.N + tk.S, ipadx=3, ipady=3, padx=3, pady=3)
status_var.set('Waiting...')

# seperator
ttk.Separator(form_frame, orient=tk.HORIZONTAL).grid(sticky='ew', row=101)

#***********
# File View
#***********

files_frame = ttk.Frame(notebook)
notebook.add(files_frame, text='Files', underline=0)
files_frame.columnconfigure(0, weight=1)
files_frame.rowconfigure(0, weight=1)

file_tree = ttk.Treeview(files_frame)
file_tree.grid(sticky='nesw')

ft_columns = ('Name', 'Type', 'Created')
file_tree.configure(columns=ft_columns)

for heading in ft_columns:
    file_tree.heading(heading, text=heading)

file_tree.configure(show='headings')

#***********************
# Functions and Bindings
#***********************

def set_theme(*args):

    theme = theme_var.get()
    style.theme_use(theme)

theme_var.trace_add('write', set_theme)

def treeview_sort_column(treeview, col, reverse):
    """ Sort a treeview column when clicked """
    data = [
        (treeview.set(iid, col), iid)
        for iid in treeview.get_children('')
    ]
    data.sort(reverse=reverse)

    for index, (sort_val, iid) in enumerate(data):
        treeview.move(iid, '', index)

    treeview.heading(
        col,
        command=lambda c=col: treeview_sort_column(file_tree, c, not reverse)
    )

for col in ft_columns:
    file_tree.heading(
        col,
        command=lambda c=col: treeview_sort_column(file_tree, c, False)
    )

def populate_treeview(*args):
    """ Look for txt and secret files to populate the treeview """
    children = file_tree.get_children()
    if children:
        file_tree.delete(*children)

    txt_files = list(Path('./test/').rglob('*.txt'))
    sec_files = list(Path('./test/').rglob('*.secret'))

    for f in (txt_files + sec_files):
        created = datetime.fromtimestamp(f.stat().st_mtime).strftime('%Y-%m-%d')
        file_tree.insert(
            '',
            tk.END,
            iid=f.name,
            values=(
                f.stem,
                f.suffix,
                created
            )
        )
populate_treeview()

def weaksauce_encrypt(text, password):
    """ Weakly and insecurely encrypt some text """
    offset = sum([ord(x) for x in password])
    encoded = ''.join(
        chr(min(ord(x) + offset, 2**20))
        for x in text
    )
    return encoded

def weaksauce_decrypt(text, password):
    """ Decrypt weakly and insecurly encrypted text """
    offset = sum([ord(x) for x in password])
    decoded = ''.join(
        chr(max(ord(x) - offset, 0))
        for x in text
    )
    return decoded

def open_file(file_path=None):
    """ Open a file """
    if not file_path:
        file_path = tkfd.askopenfilename(
            title='Select a file to open',
            filetypes=[('Secret', '*.secret'), ('Text', '*.txt')]
        )
        if not file_path:
            return

    file_path = './test/' + file_path
    filepath = Path(file_path)
    filename = filepath.stem
    category, subject = filename.split(' - ')
    message = filepath.read_text()
    if filepath.suffix == '.secret':
        password = tksd.askstring(
            'Enter password',
            'Enter the password used to '
            'encrypt the file'
        )
        # private_var.set(True) Ein kleiner Schönheitsfehler im Programm
        message = weaksauce_decrypt(message, password)
    cat_var.set(category)
    subject_var.set(subject)
    message_inp.delete('1.0', tk.END)
    message_inp.insert('1.0', message)

# open_btn.configure(command=open_file)

def save(*args):
    """ Save data to a file """
    subject = subject_var.get()
    category = cat_var.get()
    private = private_var.get()
    message = message_inp.get('1.0', tk.END)  # Start- and End-Index!

    extension = 'txt' if not private else 'secret'
    filename = f'test/{category} - {subject}.{extension}'   # little creepy filename, better ad date/time ;)
    if private:
        password = tksd.askstring(
            'Enter password',
            'Enter a password to encrypt the message!'
        )
        message = weaksauce_encrypt(message, password)

    with open(filename, 'w') as fh:
        fh.write(message)

    status_var.set(f'Message was saved to {filename}')
    tkmb.showinfo('Saved', f'Message was saved to {filename}')
    # populate_treeview()
    root.event_generate('<<FileSaved>>')

root.bind('<<FileSaved>>', populate_treeview)

save_btn.configure(command=save)

def private_warn(*arg):
    """ Warn the user of consequences of private """
    private = private_var.get()
    if private:
        response = tkmb.askokcancel(
            'Are your sure?',
            'Do you really want to encrypt this message?'
        )
        if not response:
            private_var.set(False)

private_var.trace_add('write', private_warn)

def check_filename(*args):
    """ Check if filename is already in use """
    subject = subject_var.get()
    category = cat_var.get()
    private = private_var.get()

    extension = 'txt' if not private else 'secret'
    filename = f'test/{category} - {subject}.{extension}'

    if Path(filename).exists():
        status_var.set(f'Warning {filename} already exists!')
    else:
        status_var.set('')

def set_font_size(*args):
    """ Set the font size of the text widgets font from font_size"""
    size = font_size.get()
    message_inp.configure(font=f'Default {size}')

set_font_size()
font_size.trace_add('write', set_font_size)

subject_var.trace_add('write', check_filename)
cat_var.trace_add('write', check_filename)
private_var.trace_add('write', check_filename)

# Menu
menu = tk.Menu(root)
root.configure(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='File', menu=file_menu)
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save)
file_menu.add_separator()
file_menu.add_command(label='Quit', command=root.destroy)

options_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label='Options', menu=options_menu)
options_menu.add_checkbutton(label='Private', variable=private_var)

help_menu = tk.Menu(menu, tearoff=0)
help_menu.add_command(
    label='About',
    command=lambda: tkmb.showinfo('About', 'My Tkinter Diary')
)
menu.add_cascade(label='Help', menu=help_menu)

size_menu = tk.Menu(options_menu, tearoff=0)
for size in range(6, 33, 2):
    size_menu.add_radiobutton(label=str(size), variable=font_size)

options_menu.add_cascade(menu=size_menu, label='Font Size')

theme_menu = tk.Menu(options_menu, tearoff=0)
options_menu.add_cascade(menu=theme_menu, label='Theme')

for theme in style.theme_names():
    theme_menu.add_radiobutton(
        label=theme,
        value=theme,
        variable=theme_var
    )

#*********
# Binds
#+++++++++

# Insert a signature into the Textfield is control-g is pressed
def insert_signature(event):
    message_inp.insert(tk.END, 'Tom Sol\nWizard')
message_inp.bind('<Control-Key-g>', insert_signature)

# open the selected document for m the treeview
def on_treeclick(event):
    selected = file_tree.selection()[0]
    if selected:
        open_file(selected)
        notebook.select(0)
file_tree.bind('<Double-Button-1>', on_treeclick)

# Save document at every time
root.bind_all('<Control-Key-s>', save)

# Remove warning on status label on load from treeview
# print(ttk.Entry().bindtags())
root.bind_class('TEntry', '<KeyRelease>', check_filename)
root.bind_class('TCombobox', '<KeyRelease>', check_filename)

# last line
root.mainloop()
