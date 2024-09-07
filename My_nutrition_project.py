from tkinter import *
from tkinter import messagebox
import sqlite3
from PIL import Image, ImageTk

conn = sqlite3.connect("hello.db")
root = Tk()
root.title("Party Food Planner")
root.geometry("900x500")
root.configure(bg="pale goldenrod") 


# img = ImageTk.PhotoImage()
# label = Label(root, image = img)
# label.grid(row=0, column=0)


#scroll through existing tables
def group_scroll():
    for widget in UI_Frame.winfo_children():
        if isinstance(widget, Listbox):
            widget.destroy()

    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = [table[0] for table in cursor.fetchall()]

    listbox = Listbox(UI_Frame, width=30, height=10)
    for table in tables:
        listbox.insert(END, table)
    listbox.grid(row=10, column=0, columnspan=2, padx=10, pady=10)

    def on_select(event):
        selection = listbox.curselection()
        if selection:
            selected_table = listbox.get(selection[0])
            print(f"Selected table: {selected_table}")
            display_table_contents(selected_table)

    listbox.bind("<<ListboxSelect>>", on_select)
    view_groups_label = Label(UI_Frame, text="View Groups:", font="Helvetica 13 bold")
    view_groups_label.grid(row=9, column=0, columnspan=2, pady=(20, 0))

#after the group_scroll, used to display the selected table
def display_table_contents(table_name):
    for widget in Display_Frame.winfo_children():
        widget.destroy()

    cursor = conn.execute(f"PRAGMA table_info({table_name})")
    columns = [column[1] for column in cursor.fetchall()]

    for col_num, col_name in enumerate(columns):
        label = Label(Display_Frame, text=col_name, font="Helvetica 12 bold")
        label.grid(row=0, column=col_num, padx=5, pady=3, sticky=W)

    cursor = conn.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()

    for row_num, row in enumerate(rows, start=1):
        for col_num, col_value in enumerate(row):
            label_text = f"{col_value}"
            label = Label(Display_Frame, text=label_text, font="Helvetica 12")
            label.grid(row=row_num, column=col_num, padx=5, pady=3, sticky=W)

#func for submit
def submit():
    my_firstname = FirstName_Entry.get()
    my_lastname = LastName_Entry.get()
    my_group = GroupName_Entry.get()
    my_favfood = Favfood_Entry.get()
    my_alg1 = Allergy1_Entry.get()
    my_alg2 = Allergy2_Entry.get()
    my_details = Details_Entry.get()

    cursor = conn.execute(f"PRAGMA table_info({my_group})")
    table_exists = cursor.fetchall()

    if not table_exists:
        conn.execute(f"CREATE TABLE {my_group} (id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT NOT NULL, last_name TEXT NOT NULL, group_name TEXT NOT NULL, favfood TEXT, alg1 TEXT, alg2 TEXT, details TEXT)")
        conn.commit()

    insert_query = f"INSERT INTO {my_group} (first_name, last_name, group_name, favfood, alg1, alg2, details) VALUES (?, ?, ?, ?, ?, ?, ?)"
    conn.execute(insert_query, (my_firstname, my_lastname, my_group, my_favfood, my_alg1, my_alg2, my_details))
    conn.commit()

    messagebox.showinfo("Success", "Data submitted successfully!")
    group_scroll()

# UI setup
UI_Frame = Frame(root)
UI_Frame.grid(row=0, column=0)

Title = Label(UI_Frame, text="Party Food Planner", fg='blue', font="Helvetica 15 bold")
Title.grid(row=0, column=0, columnspan=2, pady=10)

FirstName_Label = Label(UI_Frame, text="First Name: ", font="Helvetica 13 bold")
FirstName_Label.grid(row=1, column=0, sticky=W, padx=10)
FirstName_Entry = Entry(UI_Frame)
FirstName_Entry.grid(row=1, column=1, padx=10)

LastName_Label = Label(UI_Frame, text="Last Name: ", font="Helvetica 13 bold")
LastName_Label.grid(row=2, column=0, sticky=W, padx=10)
LastName_Entry = Entry(UI_Frame)
LastName_Entry.grid(row=2, column=1, padx=10)

GroupName_Label = Label(UI_Frame, text="Group Name: ", font="Helvetica 13 bold")
GroupName_Label.grid(row=3, column=0, sticky=W, padx=10)
GroupName_Entry = Entry(UI_Frame)
GroupName_Entry.grid(row=3, column=1, padx=10)

Favfood_Label = Label(UI_Frame, text="Favorite Food: ", font="Helvetica 13 bold")
Favfood_Label.grid(row=4, column=0, sticky=W, padx=10)
Favfood_Entry = Entry(UI_Frame)
Favfood_Entry.grid(row=4, column=1, padx=10)

Allergy1_Label = Label(UI_Frame, text="Allergies: ", font="Helvetica 13 bold")
Allergy1_Label.grid(row=5, column=0, sticky=W, padx=10)
Allergy1_Entry = Entry(UI_Frame)
Allergy1_Entry.grid(row=5, column=1, padx=10)

Allergy2_Label = Label(UI_Frame, text="Restricted Diets: ", font="Helvetica 13 bold")
Allergy2_Label.grid(row=6, column=0, sticky=W, padx=10)
Allergy2_Entry = Entry(UI_Frame)
Allergy2_Entry.grid(row=6, column=1, padx=10)

Details_Label = Label(UI_Frame, text="Any Other Details/Info: ", font="Helvetica 13 bold")
Details_Label.grid(row=7, column=0, sticky=W, padx=10)
Details_Entry = Entry(UI_Frame)
Details_Entry.grid(row=7, column=1, padx=10)

Submit_Button = Button(UI_Frame, text="Submit", font="Helvetica 12 bold", fg='blue', command=submit)
Submit_Button.grid(row=8, column=0, columnspan=2, pady=10, ipady=5)

# Frame to display selected table contents
Display_Frame = Frame(root, bg="white")
Display_Frame.grid(row=0, column=1, rowspan=10, padx=20, pady=10, sticky=N+S+E+W)

root.mainloop()