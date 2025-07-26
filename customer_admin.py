import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db

def open_admin_customer_window(admin_root=None):
    if admin_root:
        admin_root.withdraw()

    cust_win = tk.Toplevel()
    cust_win.title("Customer Management - Admin View")
    cust_win.geometry("1000x500")
    cust_win.configure(bg="white")

    def go_back():
        cust_win.destroy()
        if admin_root:
            admin_root.deiconify()

    tk.Button(cust_win, text="← Back", bg="#F3EDED", font=("Arial", 10, "bold"),
              command=go_back).pack(anchor="w", padx=10, pady=10)

    top_frame = tk.Frame(cust_win, bg="white")
    top_frame.pack(fill="x", padx=10)

    search_var = tk.StringVar()
    tk.Label(top_frame, text="🔍 Search: ", bg="white").pack(side="left")
    search_entry = tk.Entry(top_frame, textvariable=search_var, width=40)
    search_entry.pack(side="left", padx=5)

    btn_frame = tk.Frame(top_frame, bg="white")
    btn_frame.pack(side="right")

    tk.Button(btn_frame, text="Add", bg="#F3EDED", command=lambda: add_customer()).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Edit", bg="#F3EDED", command=lambda: edit_customer()).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Delete", bg="#F3EDED", command=lambda: delete_customer()).pack(side="left", padx=5)
    tk.Button(btn_frame, text="Refresh", bg="#F3EDED", command=lambda: refresh_table()).pack(side="left", padx=5)

    columns = ("ID", "Name", "Username", "Email", "Address")

    table_frame = tk.Frame(cust_win)
    table_frame.pack(fill="both", expand=True, padx=10, pady=10)

    hsb = tk.Scrollbar(table_frame, orient="horizontal")
    hsb.pack(side="bottom", fill="x")

    tree = ttk.Treeview(table_frame, columns=columns, show="headings",
                        xscrollcommand=hsb.set)
    hsb.config(command=tree.xview)

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=180, anchor="center")

    tree.pack(fill="both", expand=True)

    def refresh_table():
        tree.delete(*tree.get_children())
        try:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, username, email, address FROM users WHERE role = 'customer'")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            cursor.close()
            conn.close()
        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def add_customer():
        popup = tk.Toplevel(cust_win)
        popup.title("Add Customer")
        popup.geometry("350x400")

        fields = ["Name", "Username", "Email", "Address"]
        vars = {}

        for f in fields:
            tk.Label(popup, text=f).pack()
            vars[f] = tk.StringVar()
            tk.Entry(popup, textvariable=vars[f]).pack()

        def save():
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO users (name, username, email, address, role) VALUES (%s, %s, %s, %s, 'customer')",
                               (vars["Name"].get(), vars["Username"].get(), vars["Email"].get(), vars["Address"].get()))
                conn.commit()
                conn.close()
                popup.destroy()
                refresh_table()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(popup, text="Save", command=save).pack(pady=10)

    def edit_customer():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "No record selected")
            return

        data = tree.item(selected)['values']
        cid = data[0]

        popup = tk.Toplevel(cust_win)
        popup.title("Edit Customer")
        popup.geometry("350x400")

        fields = ["Name", "Username", "Email", "Address"]
        vars = {}

        for i, f in enumerate(fields):
            tk.Label(popup, text=f).pack()
            vars[f] = tk.StringVar(value=data[i + 1])
            tk.Entry(popup, textvariable=vars[f]).pack()

        def save():
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE users SET name=%s, username=%s, email=%s, address=%s WHERE id=%s",
                               (vars["Name"].get(), vars["Username"].get(), vars["Email"].get(), vars["Address"].get(), cid))
                conn.commit()
                conn.close()
                popup.destroy()
                refresh_table()
            except Exception as e:
                messagebox.showerror("Error", str(e))

        tk.Button(popup, text="Update", command=save).pack(pady=10)

    def delete_customer():
        selected = tree.focus()
        if not selected:
            messagebox.showerror("Error", "No customer selected")
            return

        cid = tree.item(selected)['values'][0]
        confirm = messagebox.askyesno("Confirm", "Delete this customer?")
        if confirm:
            try:
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("DELETE FROM users WHERE id=%s", (cid,))
                conn.commit()
                conn.close()
                refresh_table()
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def filter_search(*args):
        query = search_var.get().lower()
        for row in tree.get_children():
            values = tree.item(row)['values']
            if any(query in str(v).lower() for v in values):
                tree.item(row, tags=("match",))
            else:
                tree.item(row, tags=("no_match",))

        tree.tag_configure("match", background="white")
        tree.tag_configure("no_match", background="#f4f4f4")

    search_var.trace("w", filter_search)

    refresh_table()
