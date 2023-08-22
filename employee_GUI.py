import tkinter as tk
from tkinter import ttk
from employee_class import Employee
from employee_db_handling import insert_emp, remove_emp, update_pay, get_emps_by_name, get_all_emps, update_data


def create_entry():
    first_name = entry1.get()
    last_name = entry2.get()
    pay = entry3.get()
    emp = Employee(first_name, last_name, pay)
    insert_emp(emp)
    display_all_entrys()

# ========== Rückgabe confirm value ========== 
def confirm_values(id, value, frame, change_data_window):
        if value:
            print(value)
            remove_emp(id)
            close_change_window(frame)
            close_change_window(change_data_window)
            display_all_entrys()
        else:
            close_change_window(frame)
            
# ========== Bestätigungs-Fenster für Datensatz löschen ==========     
def confirm_delete_window(id, change_data_window):
    confirm_win = tk.Toplevel(frame_main)
    confirm_win.title("Bestätigung")
    confirm_win.geometry("200x100")
    confirm_win.configure(background="red")
    confirm_win.resizable(False, False)
    
    overlay_label = ttk.Label(confirm_win, text="Sind Sie sicher,\ndass Sie die Daten löschen wollen?")
    overlay_button1 = ttk.Button(confirm_win, text="Ja", command=lambda: confirm_values(id, True, confirm_win,change_data_window))
    overlay_button2 = ttk.Button(confirm_win, text="Nein", command=lambda: confirm_values(id, False, confirm_win,change_data_window))
    
    overlay_label.configure(background="red", padding=5)
    overlay_label.pack()
    overlay_button1.pack()
    overlay_button2.pack()
    
    center_window(confirm_win)
    
# ========== Fenster aktivieren & deaktivieren ========== 
def disable_window(frame):
    frame.attributes("-disabled", True)  # Deaktiviere das Fenster

def enable_window(frame, overlay_window):
    frame.attributes("-disabled", False)  # Aktiviere das Fenster wieder
    overlay_window.destroy()
    
def close_change_window(overlay_frame):
    frame_main.attributes("-disabled", False)  # Aktiviere das Fenster wieder
    overlay_frame.destroy()
    
# ========== Zentrierung des frame_Main ==========
def center_window(frame_main):
    frame_main.update_idletasks()  # Sorgt dafür, dass die Fenstergröße korrekt ist
    width = frame_main.winfo_width()
    height = frame_main.winfo_height()
    
    screen_width = frame_main.winfo_screenwidth()
    screen_height = frame_main.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    frame_main.geometry(f"{width}x{height}+{x}+{y}")
    

# ========== gibt die Fenstergröße zurück "width" & "height" ==========
def print_window_size():
    frame_main.update()
    width = frame_main.winfo_width()
    height = frame_main.winfo_height()
    print("Breite:", width, "Höhe:", height)
    return width, height

# =========== Fenster erstellen "frame_main" ===========
frame_main = tk.Tk()
frame_main.title("Mitarbeiter - Datenbank")
frame_main.wm_geometry('1200x600')
frame_main.configure(background='#ccc')
frame_main.resizable(False, False)

# ========= Style - Klassen =========
style = ttk.Style()
style.theme_use('default')
style.configure("Label", font=('Helvetica', 12), background='#ccc')
style.configure("Custom.TEntry", font=('Helvetica', 14), background='#ccc', foreground='black')


# =================== Table mit Daten ===================
columns = ('id', 'first_name', 'last_name', 'pay')
tree = ttk.Treeview(frame_main, columns=columns, show='headings')

def display_all_entrys():
    # clean tree-list
    for item in tree.get_children():
        tree.delete(item)
        
    contact_information = get_all_emps()
    
    # define headings
    tree.heading('id', text='ID')
    tree.heading('first_name', text='First Name')
    tree.heading('last_name', text='Last Name')
    tree.heading('pay', text='Pay')
    
    # Spaltenbreiten anpassen
    tree.column('id', width=1)
    tree.column('first_name', width=200)
    tree.column('last_name', width=200)
    tree.column('pay', width=100)
    
    # add data to the treeview
    for index, contact in enumerate(contact_information):
        if index % 2 == 0:
            tree.insert('', tk.END, values=contact, tags=("even"))
        else:
            tree.insert('', tk.END, values=contact, tags=("odd"))

    tree.tag_configure("even", background='#eee', foreground='black')
    tree.tag_configure("odd", background='#ddd', foreground='black')

    # ========= Datensatz aus Tabelle in einem extra Fenster anzeigen ========= 
    def item_selected(event):
        
        disable_window(frame_main)
        
        for selected_item in tree.selection():
            item = tree.item(selected_item)
            record = item['values']
            
            change_data_window = tk.Toplevel(frame_main)
            change_data_window.title('change Data')
            change_data_window.wm_geometry('600x200')
            change_data_window.configure(background='#ccc')
            
            # ========= erstellt inneres Fenster Style für diesen Frame =========
            frame_inner = ttk.Frame(change_data_window, width=600, height= 50, borderwidth=10, relief=tk.GROOVE)
            frame_inner.propagate(False)
            
            # Konfiguriere den Style für den inneren Frame
            inner_frame_style = ttk.Style()
            inner_frame_style.configure("Inner.TFrame", background="red")
            frame_inner.configure(style="Inner.TFrame")
            # ===================================================================
            
            # Create labels to display the selected data
            change_label1 = ttk.Label(change_data_window, text='ID:', anchor="center")
            # change_label1 = ttk.Label(change_data_window, text='ID:')
            change_label1.configure(style="Label")
            change_label1_value = ttk.Label(change_data_window, text= record[0], anchor="center")
            change_label1_value.configure(style="Label")
            
            change_label2 = ttk.Label(change_data_window, text='First Name:', anchor="center")
            change_label2.configure(style="Label")
            change_entry2_value = ttk.Entry(change_data_window)
            change_entry2_value.insert(0, record[1])
            # label2_value["state"] = "disabled"
            change_entry2_value.configure(style="Custom.TEntry")
            
            change_label3 = ttk.Label(change_data_window, text='Last Name:', anchor="center")
            change_label3.configure(style="Label")
            change_entry3_value = ttk.Entry(change_data_window)
            change_entry3_value.insert(0, record[2])
            # label3_value["state"] = "disabled"#
            change_entry3_value.configure(style="Custom.TEntry")
            
            change_label4 = ttk.Label(change_data_window, text='Pay:', anchor="center")
            change_label4.configure(style="Label")
            change_entry4_value = ttk.Entry(change_data_window)
            change_entry4_value.insert(0, record[3])
            # label4_value["state"] = "disabled"
            change_entry4_value.configure(style="Custom.TEntry")
            
            # geänderte Daten holen und Datenbank aktualisieren
            def get_change_data():
                emp = (change_label1_value["text"], change_entry2_value.get(), change_entry3_value.get(), change_entry4_value.get())
                update_data(emp)
                display_all_entrys()
            
          
            change_button1 = ttk.Button(change_data_window, text='save', command=get_change_data)
            change_button2 = ttk.Button(change_data_window, text='delete', command=lambda: confirm_delete_window(record[0], change_data_window))
            change_button3 = ttk.Button(change_data_window, text='close', command=lambda: close_change_window(change_data_window))
            
            # ================= Grid definieren ====================
            change_data_window.columnconfigure((1,6), weight = 1, uniform = 'b')
            change_data_window.columnconfigure(2, weight = 3, uniform = 'b')
            change_data_window.columnconfigure((3,4,5), weight = 10, uniform = 'b')
            change_data_window.rowconfigure((1,6), weight = 1, uniform = 'b')
            change_data_window.rowconfigure((2,3), weight = 3, uniform = 'b')
            change_data_window.rowconfigure((4,5), weight = 5, uniform = 'b')


            # Display the selected data in labels
            change_label1.grid(row=2, column=2, padx=10, pady=5, sticky="ew")
            change_label1_value.grid(row=3, column=2, padx=10, pady=5, sticky="ew")
            
            change_label2.grid(row=2, column=3, padx=10, pady=5, sticky="ew")
            change_entry2_value.grid(row=3, column=3, padx=10, pady=5, sticky="ew")
            
            change_label3.grid(row=2, column=4, padx=10, pady=5, sticky="ew")
            change_entry3_value.grid(row=3, column=4, padx=10, pady=5, sticky="ew")
            
            change_label4.grid(row=2, column=5, padx=10, pady=5, sticky="ew")
            change_entry4_value.grid(row=3, column=5, padx=10, pady=5, sticky="ew")
            
            change_button1.grid(row=4, column=5, padx=10, pady=5, sticky="ew")
            change_button2.grid(row=4, column=4, padx=10, pady=5, sticky="ew")
            change_button3.grid(row=5, column=5, padx=10, pady=5, sticky="ew")
            
            center_window(change_data_window)
            
            change_data_window.protocol("WM_DELETE_WINDOW", lambda: enable_window(frame_main, change_data_window))

            
    tree.bind('<Double-1>', item_selected)

display_all_entrys()
# =================================================

label1 = ttk.Label(frame_main, text="first name", style = 'Label')
label2 = ttk.Label(frame_main, text="last name", style = 'Label')
label3 = ttk.Label(frame_main, text="pay", style = 'Label')

entry1 = ttk.Entry(frame_main, style='Custom.TEntry')
entry2 = ttk.Entry(frame_main, style='Custom.TEntry')
entry3 = ttk.Entry(frame_main, style='Custom.TEntry')

button1 = ttk.Button(frame_main, text="create", command=create_entry)
button2 = ttk.Button(frame_main, text="update", command=print_window_size)
button3 = ttk.Button(frame_main, text="delete", command=print_window_size)
button4 = ttk.Button(frame_main, text="quit", command=frame_main.destroy)

# ================= Grid definieren ====================
# frame_main.columnconfigure((0,1,2), weight = 1, uniform = 'a')
frame_main.columnconfigure(1, weight = 1, uniform = 'a')
frame_main.columnconfigure(2, weight = 12, uniform = 'a')
frame_main.columnconfigure(3, weight = 1, uniform = 'a')
frame_main.columnconfigure((4,5,6,7), weight = 2, uniform = 'a')
frame_main.columnconfigure(8, weight = 1, uniform = 'a')
frame_main.rowconfigure((1,2,3,4,5,6), weight = 1, uniform = 'a')
frame_main.rowconfigure(7, weight = 5, uniform = 'a')
frame_main.rowconfigure(8, weight = 1, uniform = 'a')
frame_main.rowconfigure(9, weight = 1, uniform = 'a')

# ================= Widgets platzieren =================
tree.grid(row = 2, column = 2, rowspan = 7, sticky="nsew")

label1.grid(row = 2, column = 4, sticky="nesw", padx = 3, pady = 3)
label2.grid(row = 3, column = 4, sticky="nesw", padx = 3, pady = 3)
label3.grid(row = 4, column = 4, sticky="nesw", padx = 3, pady = 3) 

entry1.grid(row = 2, column = 5, columnspan=3, sticky="nesw", padx = 3, pady = 6)
entry2.grid(row = 3, column = 5, columnspan=3, sticky="nesw", padx = 3, pady = 6)
entry3.grid(row = 4, column = 5, columnspan=3, sticky="nesw", padx = 3, pady = 6)

button1.grid(row = 5, column = 5, columnspan=3, sticky="nesw", padx = 3, pady = 6)
button4.grid(row = 8, column = 6, columnspan=2, sticky="nesw", padx = 3, pady = 6)




center_window(frame_main)
win_size = print_window_size()
print(win_size)

# for item in tree.keys():
#     print(item, ": ", tree[item])

frame_main.mainloop()


