import tkinter as tk
from tkinter import ttk, messagebox
from db import connect_db  # Ensure your db.py has connect_db()
from customer_admin import open_admin_customer_window

def show_admin_panel():
    admin_root = tk.Tk()
    admin_root.title("Admin Panel")
    admin_root.geometry("400x300")

    # ---- Open Inventory Window ----
    def open_inventory_window():
        admin_root.withdraw()
        inv_win = tk.Toplevel()
        inv_win.title("Product Inventory")
        inv_win.geometry("900x600")

        # --- BACK BUTTON ---
        def go_back():
            inv_win.destroy()
            admin_root.deiconify()

        tk.Button(inv_win, text="← Back", font=("Arial", 10, "bold"),
                  bg="#F3EDED", command=go_back).pack(anchor="w", padx=5, pady=5)

        # --- Top controls (Search + Buttons) ---
        top_frame = tk.Frame(inv_win)
        top_frame.pack(fill="x", padx=10, pady=5)

        search_var = tk.StringVar()
        tk.Label(top_frame, text="🔍 Search:").pack(side="left")
        search_entry = tk.Entry(top_frame, textvariable=search_var, width=30)
        search_entry.pack(side="left", padx=5)

        # Button frame
        btn_frame = tk.Frame(top_frame)
        btn_frame.pack(side="right")

        tk.Button(btn_frame, text="➕ Add", bg="#F3EDED", command=lambda: add_product()).pack(side="left", padx=5)
        tk.Button(btn_frame, text="✏️ Edit", bg="#F3EDED", command=lambda: edit_product()).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🗑️ Delete", bg="#F3EDED", command=lambda: delete_product()).pack(side="left", padx=5)
        tk.Button(btn_frame, text="🔁 Refresh", bg="#F3EDED", command=lambda: refresh_products()).pack(side="left", padx=5)

        # --- Table with scrollbar ---
        table_frame = tk.Frame(inv_win)
        table_frame.pack(expand=True, fill="both", padx=10, pady=10)
        columns = ("ID", "Name", "Price", "Category", "Remaining Pieces")

        scrollbar = tk.Scrollbar(table_frame)
        scrollbar.pack(side="right", fill="y")

        tree = ttk.Treeview(table_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=tree.yview)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        tree.pack(expand=True, fill="both")

        # --- Function Definitions ---
        def refresh_products():
            tree.delete(*tree.get_children())
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, price, category, remaining_pieces FROM products")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

        def search_products(*args):
            query = search_var.get().lower()
            tree.delete(*tree.get_children())
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, price, category FROM products")
            for row in cursor.fetchall():
                if query in str(row[1]).lower() or query in str(row[3]).lower():
                    tree.insert("", "end", values=row)
            conn.close()

        search_var.trace("w", search_products)

        def delete_product():
            selected = tree.focus()
            if not selected:
                messagebox.showerror("Error", "No product selected.")
                return
            pid = tree.item(selected)['values'][0]
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM products WHERE id=%s", (pid,))
            conn.commit()
            conn.close()
            refresh_products()

        def add_product():
            def save():
                name = name_var.get()
                price = price_var.get()
                cat = cat_var.get()
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("INSERT INTO products (name, price, category) VALUES (%s, %s, %s)",
                               (name, price, cat))
                conn.commit()
                conn.close()
                top.destroy()
                refresh_products()

            top = tk.Toplevel(inv_win)
            top.title("Add Product")
            name_var = tk.StringVar()
            price_var = tk.DoubleVar()
            cat_var = tk.StringVar()

            tk.Label(top, text="Name:").pack()
            tk.Entry(top, textvariable=name_var).pack()
            tk.Label(top, text="Price:").pack()
            tk.Entry(top, textvariable=price_var).pack()
            tk.Label(top, text="Category:").pack()
            tk.Entry(top, textvariable=cat_var).pack()
            tk.Button(top, text="Save", command=save).pack(pady=5)

        def edit_product():
            selected = tree.focus()
            if not selected:
                messagebox.showerror("Error", "No product selected.")
                return
            pid, name, price, cat, _ = tree.item(selected)['values']

            def save():
                new_name = name_var.get()
                new_price = price_var.get()
                new_cat = cat_var.get()
                conn = connect_db()
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET name=%s, price=%s, category=%s WHERE id=%s",
                               (new_name, new_price, new_cat, pid))
                conn.commit()
                conn.close()
                top.destroy()
                refresh_products()

            top = tk.Toplevel(inv_win)
            top.title("Edit Product")
            name_var = tk.StringVar(value=name)
            price_var = tk.DoubleVar(value=price)
            cat_var = tk.StringVar(value=cat)

            tk.Label(top, text="Name:").pack()
            tk.Entry(top, textvariable=name_var).pack()
            tk.Label(top, text="Price:").pack()
            tk.Entry(top, textvariable=price_var).pack()
            tk.Label(top, text="Category:").pack()
            tk.Entry(top, textvariable=cat_var).pack()
            tk.Button(top, text="Update", command=save).pack(pady=5)

        refresh_products()

    # ---- Open Customer Window ----
    def open_customer_window():
        admin_root.withdraw()
        cust_win = tk.Toplevel()
        cust_win.title("Customer Info")
        cust_win.geometry("600x400")

        # --- BACK BUTTON ---
        def back():
            cust_win.destroy()
            admin_root.deiconify()

        tk.Button(cust_win, text="← Back", font=("Arial", 10, "bold"),
                  bg="#F3EDED", command=back).pack(anchor="w", padx=5, pady=5)

        tree = ttk.Treeview(cust_win, columns=("ID", "Name", "Phone"), show="headings")
        for col in ("ID", "Name", "Phone"):
            tree.heading(col, text=col)
            tree.column(col, width=150)
        tree.pack(expand=True, fill="both")

        def refresh_customers():
            tree.delete(*tree.get_children())
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, phone FROM customers")
            for row in cursor.fetchall():
                tree.insert("", "end", values=row)
            conn.close()

        refresh_customers()

    # ---- Admin Main Buttons ----
    tk.Label(admin_root, text="Admin Dashboard", font=("Arial", 16, "bold")).pack(pady=10)
    tk.Button(admin_root, text="Manage Inventory", width=25, bg="#87CEFA", command=open_inventory_window).pack(pady=10)
    tk.Button(admin_root, text="👤 Customer Info", width=25, bg="#90EE90", command=lambda: open_admin_customer_window(admin_root)).pack()

    admin_root.mainloop()
