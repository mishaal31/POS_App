import tkinter as tk
from tkinter import messagebox
from db import connect_db
from fpdf import FPDF
from datetime import datetime
import os
import random
from cart import clear_cart 


def show_receipt(root, cart, cart_listbox, total_label, discount_label, tax_label, final_label, payment_method, discount_var):
    if not cart:
        messagebox.showwarning("Warning", "Cart is empty!")
        return

    # --- Generate date, time, customer ID ---
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    customer_id = f"CUST{random.randint(1000, 9999)}"

    # --- Tkinter Window for Receipt Preview ---
    receipt = tk.Toplevel(root)
    receipt.title("Receipt")
    receipt.geometry("400x500+300+200")
    receipt.lift()
    receipt.focus_force()

    text = tk.Text(receipt, width=50, height=25)
    text.pack()

    # --- Receipt Header ---
    text.insert(tk.END, "             Skin Care Shop\n\n")
    text.insert(tk.END, f"Customer ID: {customer_id}\nDate: {date_str} {time_str}\n")
    text.insert(tk.END, "-" * 42 + "\n")
    text.insert(tk.END, f"{'Item':20}{'Price (Rs.)':>20}\n")
    text.insert(tk.END, "-" * 42 + "\n")

    lines = []
    lines.append("           Skin Care Shop")
    lines.append(f"Customer ID: {customer_id}    Date: {date_str} {time_str}")
    lines.append("-" * 42)
    lines.append(f"{'Item':20}{'Price (Rs.)':>20}")
    lines.append("-" * 42)

    # --- Items ---
    for item in cart:
        name = item['name'][:20]
        price = f"{item['price']:.2f}"
        text.insert(tk.END, f"{name:20}{price:>20}\n")
        lines.append(f"{name:20}{price:>20}")

    # --- Calculations ---
    total = sum(item["price"] for item in cart)
    tax_percent = 15 if payment_method.get() == "Cash" else 5
    tax_amount = total * tax_percent / 100
    grand_total = total + tax_amount

    text.insert(tk.END, "-" * 42 + "\n")
    text.insert(tk.END, f"{'Total:':20}{total:>20.2f}\n")
    text.insert(tk.END, f"{'Tax (' + str(tax_percent) + '%):':20}{tax_amount:>20.2f}\n")
    text.insert(tk.END, f"{'Grand Total:':20}{grand_total:>20.2f}\n")
    text.insert(tk.END, f"{'Paid via:':20}{payment_method.get():>20}\n")
    text.insert(tk.END, "-" * 42 + "\n")

    lines.append("-" * 42)
    lines.append(f"{'Total:':20}{total:>20.2f}")
    lines.append(f"{'Tax (' + str(tax_percent) + '%):':20}{tax_amount:>20.2f}")
    lines.append(f"{'Grand Total:':20}{grand_total:>20.2f}")
    lines.append(f"{'Paid via:':20}{payment_method.get():>20}")
    lines.append("-" * 42)

    # --- Save as PDF ---
    if not os.path.exists("invoices"):
        os.makedirs("invoices")

    filename = f"invoices/receipt_{now.strftime('%Y%m%d_%H%M%S')}.pdf"
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    for line in lines:
        pdf.cell(200, 10, txt=line.strip(), ln=True)

    pdf.output(filename)
    messagebox.showinfo("Receipt Saved", f"PDF saved as:\n{filename}")

    # --- Save Bill, Bill Items & Sales in DB ---
    conn = connect_db()
    cursor = conn.cursor()

    # Generate one transaction ID for this checkout
    transaction_id = f"TXN-{int(datetime.now().timestamp())}-{customer_id}"

    # 1. Insert Bill
    cursor.execute("INSERT INTO bills (user_id, total) VALUES (%s, %s)", (customer_id, grand_total))
    bill_id = cursor.lastrowid

    # 2. Insert Bill Items + Sales
    for item in cart:
        cursor.execute("SELECT id, price, stock_boxes, pieces_per_box FROM products WHERE name=%s", (item['name'],))
        result = cursor.fetchone()
        if result:
            product_id, db_price, stock_boxes, pieces_per_box = result

            # Use cart price (discounted), else DB price
            sale_price = item.get('price', db_price)

            # Insert into bill_items
            cursor.execute(
                "INSERT INTO bill_items (bill_id, product_id, quantity, price_at_sale) VALUES (%s, %s, %s, %s)",
                (bill_id, product_id, 1, sale_price)
            )

            # Insert into sales (all items share one transaction_id)
            cursor.execute(
                "INSERT INTO sales (transaction_id, user_id, product_id, quantity, price_at_sale) VALUES (%s, %s, %s, %s, %s)",
                (transaction_id, customer_id, product_id, 1, sale_price)
            )

            # --- Stock update logic ---
            if pieces_per_box > 1:
                pieces_per_box -= 1
            else:
                if stock_boxes > 0:
                    stock_boxes -= 1
                    # Reset pieces_per_box to a full box again (you may need a product field "pieces_default")
                    pieces_per_box = result[3]  
                else:
                    messagebox.showwarning("Stock", f"{item['name']} is out of stock!")

            cursor.execute(
                "UPDATE products SET stock_boxes=%s, pieces_per_box=%s WHERE id=%s",
                (stock_boxes, pieces_per_box, product_id)
            )

    conn.commit()
    conn.close()

    # --- Clear the cart after checkout ---
    clear_cart(cart, cart_listbox, total_label, discount_label, tax_label, final_label)
