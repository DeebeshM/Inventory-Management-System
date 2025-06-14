import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

# --- DATABASE SETUP ---
def init_db():
    with sqlite3.connect("inventory.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS inventory (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                quantity INTEGER NOT NULL,
                price REAL NOT NULL
            )
        """)
        conn.commit()

# --- LOGIN FUNCTIONALITY ---
def check_login():
    user = username_entry.get()
    pwd = password_entry.get()
    if user == "admin" and pwd == "admin123":
        login_window.destroy()
        show_main_window()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password")

# --- MAIN INVENTORY WINDOW ---
def show_main_window():
    root = tk.Tk()
    root.title("Inventory Management System")
    root.geometry("900x650")
    root.configure(bg="#f0f4f7")

    # --- STYLING ---
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=35,
                    fieldbackground="white",
                    font=('Segoe UI', 12))
    style.map("Treeview", background=[('selected', '#007bff')])
    style.configure("TButton",
                    font=('Segoe UI', 13, 'bold'),
                    padding=10)
    style.configure("Header.TLabel",
                    font=("Segoe UI", 24, "bold"),
                    foreground="#0d6efd",
                    background="#f0f4f7")

    # --- FUNCTIONS ---
    def add_product():
        name = name_entry.get()
        qty = quantity_entry.get()
        price = price_entry.get()
        if name and qty and price:
            try:
                with sqlite3.connect("inventory.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("INSERT INTO inventory (name, quantity, price) VALUES (?, ?, ?)",
                                   (name, int(qty), float(price)))
                    conn.commit()
                clear_entries()
                load_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showwarning("Input Error", "Please fill all fields.")

    def update_product():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a product to update.")
            return
        item_id = tree.item(selected)['values'][0]
        name = name_entry.get()
        qty = quantity_entry.get()
        price = price_entry.get()
        if name and qty and price:
            try:
                with sqlite3.connect("inventory.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute("UPDATE inventory SET name=?, quantity=?, price=? WHERE id=?",
                                   (name, int(qty), float(price), item_id))
                    conn.commit()
                clear_entries()
                load_data()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def delete_product():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Selection Error", "Please select a product to delete.")
            return
        item_id = tree.item(selected)['values'][0]
        try:
            with sqlite3.connect("inventory.db") as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM inventory WHERE id=?", (item_id,))
                conn.commit()
            clear_entries()
            load_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def load_data():
        tree.delete(*tree.get_children())
        with sqlite3.connect("inventory.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM inventory")
            for row in cursor.fetchall():
                tree.insert("", tk.END, values=row)

    def select_item(event):
        selected = tree.focus()
        if not selected:
            return
        values = tree.item(selected, 'values')
        clear_entries()
        name_entry.insert(0, values[1])
        quantity_entry.insert(0, values[2])
        price_entry.insert(0, values[3])

    def clear_entries():
        name_entry.delete(0, tk.END)
        quantity_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)

    # --- HEADER ---
    header = ttk.Label(root, text="Inventory Management System", style="Header.TLabel")
    header.pack(pady=25)

    # --- FORM FRAME ---
    form_frame = tk.Frame(root, bg="#f0f4f7")
    form_frame.pack(pady=15)

    tk.Label(form_frame, text="Product Name:", font=('Segoe UI', 14), bg="#f0f4f7").grid(row=0, column=0, padx=20, pady=12, sticky='e')
    name_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 14))
    name_entry.grid(row=0, column=1, pady=12)

    tk.Label(form_frame, text="Quantity:", font=('Segoe UI', 14), bg="#f0f4f7").grid(row=1, column=0, padx=20, pady=12, sticky='e')
    quantity_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 14))
    quantity_entry.grid(row=1, column=1, pady=12)

    tk.Label(form_frame, text="Price:", font=('Segoe UI', 14), bg="#f0f4f7").grid(row=2, column=0, padx=20, pady=12, sticky='e')
    price_entry = tk.Entry(form_frame, width=35, font=('Segoe UI', 14))
    price_entry.grid(row=2, column=1, pady=12)

    # --- BUTTON FRAME ---
    btn_frame = tk.Frame(root, bg="#f0f4f7")
    btn_frame.pack(pady=15)

    ttk.Button(btn_frame, text="Add", command=add_product).grid(row=0, column=0, padx=20, pady=15, ipadx=15, ipady=7)
    ttk.Button(btn_frame, text="Update", command=update_product).grid(row=0, column=1, padx=20, pady=15, ipadx=15, ipady=7)
    ttk.Button(btn_frame, text="Delete", command=delete_product).grid(row=0, column=2, padx=20, pady=15, ipadx=15, ipady=7)
    ttk.Button(btn_frame, text="Clear", command=clear_entries).grid(row=0, column=3, padx=20, pady=15, ipadx=15, ipady=7)

    # --- TREEVIEW ---
    tree_frame = tk.Frame(root)
    tree_frame.pack(pady=25)

    columns = ("ID", "Name", "Quantity", "Price")
    tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=200 if col == "Name" else 120)

    tree.pack()
    tree.bind("<<TreeviewSelect>>", select_item)

    load_data()
    root.mainloop()

# --- RUN EVERYTHING ---
init_db()

# --- LOGIN WINDOW ---
login_window = tk.Tk()
login_window.title("Login - Inventory System")
login_window.geometry("450x320")
login_window.configure(bg="#e6f0fa")

tk.Label(login_window, text="Login", font=("Segoe UI", 26, "bold"), bg="#e6f0fa", fg="#0d6efd").pack(pady=30)

form = tk.Frame(login_window, bg="#e6f0fa")
form.pack()

tk.Label(form, text="Username:", font=("Segoe UI", 16), bg="#e6f0fa").grid(row=0, column=0, padx=20, pady=15)
username_entry = tk.Entry(form, width=28, font=('Segoe UI', 16))
username_entry.grid(row=0, column=1)

tk.Label(form, text="Password:", font=("Segoe UI", 16), bg="#e6f0fa").grid(row=1, column=0, padx=20, pady=15)
password_entry = tk.Entry(form, show="*", width=28, font=('Segoe UI', 16))
password_entry.grid(row=1, column=1)

tk.Button(login_window, text="Login", width=20, bg="#0d6efd", fg="white",
          font=("Segoe UI", 14, "bold"), command=check_login).pack(pady=25, ipadx=5, ipady=7)

login_window.mainloop()
