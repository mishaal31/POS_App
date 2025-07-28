import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from cart import setup_cart_ui, add_to_cart, remove_selected_item
from customer import open_customer_form
from registeration import show_login
from recepit import show_receipt
from db import connect_db
from category import get_categories, show_category

def get_products_from_db():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT name, price, category, image FROM products")
    products = cursor.fetchall()
    conn.close()
    return products

def show_main_pos():
    root = tk.Tk()
    root.title("Skincare POS")
    root.geometry("1000x600")

    products = get_products_from_db()
    cart = []
    payment_method = tk.StringVar(value="Cash")
    discount_var = tk.StringVar(value="0")

    # Top frame for Customer + Category only
    top_frame = tk.Frame(root)
    top_frame.pack(side=tk.TOP, fill=tk.X)

    # Main layout frame
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    product_frame = tk.Frame(main_frame)
    product_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    cart_frame = tk.Frame(main_frame, width=300, bd=2, relief="sunken")
    cart_frame.pack(side=tk.RIGHT, fill=tk.Y)

    tk.Label(cart_frame, text="Cart").pack(pady=5)

    # Setup cart UI and get UI elements
    cart_ui = setup_cart_ui(cart_frame)
    cart_listbox, total_label, discount_label, tax_label, final_label = cart_ui

    # Remove item button
    tk.Button(cart_frame, text="Remove Item", command=lambda: remove_selected_item(
        cart, cart_listbox, total_label, discount_label, tax_label, final_label, discount_var, payment_method
    )).pack(pady=2)

    # Payment method selection
    tk.Label(cart_frame, text="Payment Method:").pack(pady=2)
    tk.Radiobutton(cart_frame, text="Cash", variable=payment_method, value="Cash").pack()
    tk.Radiobutton(cart_frame, text="Card", variable=payment_method, value="Card").pack()

    # ✅ Corrected Checkout Button
    tk.Button(cart_frame, text="Checkout", command=lambda: show_receipt(
        root, cart, cart_listbox, total_label, discount_label, tax_label, final_label, payment_method, discount_var
    )).pack(pady=10)

    # Show all products initially
    show_category("All", product_frame, products, cart, cart_listbox,
                  total_label, discount_label, tax_label, final_label,
                  discount_var, payment_method, add_to_cart)

    root.mainloop()
