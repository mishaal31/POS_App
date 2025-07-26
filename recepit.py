import tkinter as tk
from tkinter import messagebox

def show_receipt(root, cart, payment_method, discount_var):
    if not cart:
        messagebox.showwarning("Warning", "Cart is empty!")
        return

    receipt = tk.Toplevel(root)
    receipt.title("Receipt")

    text = tk.Text(receipt, width=40, height=20)
    text.pack()

    text.insert(tk.END, "------- Coffee Shop Receipt -------\n")
    for item in cart:
        text.insert(tk.END, f"{item['name']} - Rs.{item['price']}\n")

    total = sum(item["price"] for item in cart)
    discount_percent = int(discount_var.get())
    discount_amount = total * discount_percent / 100
    subtotal = total - discount_amount

    tax_percent = 15 if payment_method.get() == "Cash" else 5
    tax_amount = subtotal * tax_percent / 100
    grand_total = subtotal + tax_amount

    text.insert(tk.END, f"\nTotal: Rs. {total}")
    text.insert(tk.END, f"\nDiscount ({discount_percent}%): -Rs.{discount_amount}")
    text.insert(tk.END, f"\nTax ({tax_percent}%): Rs.{tax_amount}")
    text.insert(tk.END, f"\nGrand Total: Rs.{grand_total:.2f}")
    text.insert(tk.END, f"\nPaid via: {payment_method.get()}")
    text.insert(tk.END, "\n----------------------------------")
