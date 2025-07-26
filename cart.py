from tkinter import *
from tkinter import messagebox

def setup_cart_ui(parent):
    cart_listbox = Listbox(parent, width=40)
    cart_listbox.pack(pady=5)

    total_label = Label(parent, text="Total: 0")
    total_label.pack()

    discount_label = Label(parent, text="Discount: 0")
    discount_label.pack()

    tax_label = Label(parent, text="Tax: 0")
    tax_label.pack()

    final_label = Label(parent, text="Final: 0")
    final_label.pack()

    return cart_listbox, total_label, discount_label, tax_label, final_label

def add_to_cart(product, cart, cart_listbox,
                total_label, discount_label, tax_label, final_label,
                discount_var, payment_method):
    cart.append(product)
    cart_listbox.insert(END, f"{product['name']} - Rs {product['price']}")

    update_totals(cart, total_label, discount_label, tax_label, final_label, discount_var, payment_method)

def remove_selected_item(cart, cart_listbox,
                         total_label, discount_label, tax_label, final_label,
                         discount_var, payment_method):
    selected_index = cart_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        cart.pop(index)
        cart_listbox.delete(index)
        update_totals(cart, total_label, discount_label, tax_label, final_label, discount_var, payment_method)
    else:
        messagebox.showwarning("Remove", "Please select item to remove.")

def update_totals(cart, total_label, discount_label, tax_label, final_label, discount_var, payment_method):
    total = sum(float(p['price']) for p in cart)
    discount = float(discount_var.get()) if discount_var.get().isdigit() else 0
    discount_amount = (discount / 100) * total
    subtotal = total - discount_amount

    tax_rate = 0.15 if payment_method.get() == "Cash" else 0.05
    tax = subtotal * tax_rate
    final = subtotal + tax


    discount_label.config(text=f"Discount: Rs {discount_amount:.2f}")
    tax_label.config(text=f"Tax: Rs {tax:.2f}")
    final_label.config(text=f"Total: Rs {final:.2f}")
