from tkinter import *
from tkinter import messagebox

def setup_cart_ui(parent):
    cart_listbox = Listbox(parent, width=40)
    cart_listbox.pack(pady=5)

    total_label = Label(parent, text="")
    discount_label = Label(parent, text="")
    tax_label = Label(parent, text="")
    final_label = Label(parent, text="")

    # Don't pack yet — only pack when cart has items
    return cart_listbox, total_label, discount_label, tax_label, final_label

def add_to_cart(product, cart, cart_listbox,
                total_label, discount_label, tax_label, final_label,
                discount_var, payment_method):
    cart.append(product)
    cart_listbox.insert(END, f"{product['name']} - Rs {product['price']}")

    # Show labels only when cart has items
    if cart:
        total_label.pack()
        tax_label.pack()
        final_label.pack()

    update_totals(cart, total_label, discount_label, tax_label, final_label, discount_var, payment_method)

def remove_selected_item(cart, cart_listbox,
                         total_label, discount_label, tax_label, final_label,
                         discount_var, payment_method):
    selected_index = cart_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        cart.pop(index)
        cart_listbox.delete(index)

        if not cart:
            # Hide labels when cart is empty
            total_label.pack_forget()
            discount_label.pack_forget()
            tax_label.pack_forget()
            final_label.pack_forget()

        update_totals(cart, total_label, discount_label, tax_label, final_label, discount_var, payment_method)
    else:
        messagebox.showwarning("Remove", "Please select item to remove.")

def update_totals(cart, total_label, discount_label, tax_label, final_label, discount_var, payment_method):
    if not cart:
        return

    total = sum(float(p['price']) for p in cart)
    discount = float(discount_var.get()) if discount_var.get().isdigit() else 0
    discount_amount = (discount / 100) * total
    subtotal = total - discount_amount

    tax_rate = 0.15 if payment_method.get() == "Cash" else 0.05
    tax = subtotal * tax_rate
    final = subtotal + tax

    total_label.config(text=f"Subtotal: Rs {total:.2f}")
    tax_label.config(text=f"Tax: Rs {tax:.2f}")
    final_label.config(text=f"Total: Rs {final:.2f}")

def clear_cart(cart, cart_listbox, total_label, discount_label, tax_label, final_label):
    cart.clear()
    cart_listbox.delete(0, END)
    total_label.pack_forget()
    discount_label.pack_forget()
    tax_label.pack_forget()
    final_label.pack_forget()
