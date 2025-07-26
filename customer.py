# customer.py
import tkinter as tk
from tkinter import ttk, messagebox

customer_data = []  
def open_customer_form(root):
    form = tk.Toplevel(root)
    form.title("Customer Details")

    def add_customer():
        name = name_entry.get()
        phone = phone_entry.get()
        if name and phone:
            customer_data.append((name, phone))
            refresh_customer_list()
            messagebox.showinfo("Success", "Customer added!")

    def edit_customer():
        selected = customer_tree.selection()
        if selected:
            index = int(selected[0])
            name = name_entry.get()
            phone = phone_entry.get()
            if name and phone:
                customer_data[index] = (name, phone)
                refresh_customer_list()
                messagebox.showinfo("Updated", "Customer updated!")

    def delete_customer():
        selected = customer_tree.selection()
        if selected:
            index = int(selected[0])
            del customer_data[index]
            refresh_customer_list()
            messagebox.showinfo("Deleted", "Customer deleted!")

    def refresh_customer_list():
        customer_tree.delete(*customer_tree.get_children())
        for i, (name, phone) in enumerate(customer_data):
            customer_tree.insert("", "end", iid=i, values=(name, phone))

    # UI Setup
    tk.Label(form, text="Name:").grid(row=0, column=0, padx=5, pady=5)
    name_entry = tk.Entry(form)
    name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form, text="Phone:").grid(row=1, column=0, padx=5, pady=5)
    phone_entry = tk.Entry(form)
    phone_entry.grid(row=1, column=1, padx=5, pady=5)

    btn_frame = tk.Frame(form)
    btn_frame.grid(row=2, column=0, columnspan=2, pady=10)

    tk.Button(btn_frame, text="Add", command=add_customer).grid(row=0, column=0, padx=5)
    tk.Button(btn_frame, text="Edit", command=edit_customer).grid(row=0, column=1, padx=5)
    tk.Button(btn_frame, text="Delete", command=delete_customer).grid(row=0, column=2, padx=5)

    customer_tree = ttk.Treeview(form, columns=("Name", "Phone"), show="headings")
    customer_tree.heading("Name", text="Name")
    customer_tree.heading("Phone", text="Phone")
    customer_tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    refresh_customer_list()
