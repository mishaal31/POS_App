import tkinter as tk
from tkinter import messagebox
from db import connect_db
from fpdf import FPDF
from datetime import datetime
import os
import random

def show_receipt(root, cart, payment_method, discount_var):
    if not cart:
        messagebox.showwarning("Warning", "Cart is empty!")
        return

    # Generate date, time, and customer ID
    now = datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")
    customer_id = f"CUST{random.randint(1000,9999)}"

    # --- Tkinter Window for Receipt Preview ---
    receipt = tk.Toplevel(root)
    receipt.title("Receipt")
    receipt.geometry("400x500+300+200")
    receipt.lift()
    receipt.focus_force()

    receipt.title("Receipt")

    text = tk.Text(receipt, width=50, height=25)
    text.pack()

    # Header
    text.insert(tk.END, "             Skin Care Shop\n\n")
    text.insert(tk.END, f"Customer ID: {customer_id}    Date: {date_str} {time_str}\n")
    text.insert(tk.END, "-"*42 + "\n")
    text.insert(tk.END, f"{'Item':20}{'Price (Rs.)':>20}\n")
    text.insert(tk.END, "-"*42 + "\n")

    lines = []
    lines.append("           Skin Care Shop")
    lines.append(f"Customer ID: {customer_id}    Date: {date_str} {time_str}")
    lines.append("-" * 42)
    lines.append(f"{'Item':20}{'Price (Rs.)':>20}")
    lines.append("-" * 42)

    # Items
    for item in cart:
        name = item['name'][:20]  # limit to 20 chars
        price = f"{item['price']:.2f}"
        text.insert(tk.END, f"{name:20}{price:>20}\n")
        lines.append(f"{name:20}{price:>20}")

    # Calculations
    total = sum(item["price"] for item in cart)
    discount_percent = int(discount_var.get())
    discount_amount = total * discount_percent / 100
    subtotal = total - discount_amount

    tax_percent = 15 if payment_method.get() == "Cash" else 5
    tax_amount = subtotal * tax_percent / 100
    grand_total = subtotal + tax_amount

    text.insert(tk.END, "-"*42 + "\n")
    text.insert(tk.END, f"{'Total:':20}{total:>20.2f}\n")
    text.insert(tk.END, f"{'Discount (' + str(discount_percent) + '%):':20}- {discount_amount:>19.2f}\n")
    text.insert(tk.END, f"{'Tax (' + str(tax_percent) + '%):':20}{tax_amount:>20.2f}\n")
    text.insert(tk.END, f"{'Grand Total:':20}{grand_total:>20.2f}\n")
    text.insert(tk.END, f"{'Paid via:':20}{payment_method.get():>20}\n")
    text.insert(tk.END, "-"*42 + "\n")

    lines.append("-" * 42)
    lines.append(f"{'Total:':20}{total:>20.2f}")
    lines.append(f"{'Discount (' + str(discount_percent) + '%):':20}- {discount_amount:>19.2f}")
    lines.append(f"{'Tax (' + str(tax_percent) + '%):':20}{tax_amount:>20.2f}")
    lines.append(f"{'Grand Total:':20}{grand_total:>20.2f}")
    lines.append(f"{'Paid via:':20}{payment_method.get():>20}")
    lines.append("-" * 42)

    # --- Save as PDF in 'invoices/' folder ---
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

    # --- Deduct stock from database ---
    conn = connect_db()
    cursor = conn.cursor()

    for item in cart:
        cursor.execute("SELECT id, stock_boxes, pieces_per_box FROM products WHERE name=%s", (item['name'],))
        result = cursor.fetchone()
        if result:
            product_id, boxes, pieces = result
            if pieces > 1:
                pieces -= 1
            elif boxes > 0:
                boxes -= 1
                pieces = 9  # assuming 10 per box
            else:
                pieces = 0

            cursor.execute(
                "UPDATE products SET stock_boxes=%s, pieces_per_box=%s WHERE id=%s",
                (boxes, pieces, product_id)
            )

    conn.commit()
    conn.close()


