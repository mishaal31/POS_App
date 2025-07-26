import tkinter as tk
from tkinter import messagebox
from db import connect_db
from fpdf import FPDF
from datetime import datetime
import os

def show_receipt(root, cart, payment_method, discount_var):
    if not cart:
        messagebox.showwarning("Warning", "Cart is empty!")
        return

    # --- Tkinter Window for Receipt Preview ---
    receipt = tk.Toplevel(root)
    receipt.title("Receipt")

    text = tk.Text(receipt, width=40, height=20)
    text.pack()

    text.insert(tk.END, "------- Coffee Shop Receipt -------\n")
    lines = ["------- Coffee Shop Receipt -------"]

    for item in cart:
        line = f"{item['name']} - Rs.{item['price']}"
        text.insert(tk.END, line + "\n")
        lines.append(line)

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

    lines.append(f"\nTotal: Rs. {total}")
    lines.append(f"Discount ({discount_percent}%): -Rs.{discount_amount}")
    lines.append(f"Tax ({tax_percent}%): Rs.{tax_amount}")
    lines.append(f"Grand Total: Rs.{grand_total:.2f}")
    lines.append(f"Paid via: {payment_method.get()}")
    lines.append("----------------------------------")

    # --- Save as PDF in 'invoice/' folder ---
    if not os.path.exists("invoices"):
        os.makedirs("invoices")

    filename = f"invoices/receipt_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
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
