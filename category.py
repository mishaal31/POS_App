import tkinter as tk
from PIL import Image, ImageTk
import os
from cart import add_to_cart

# Categories list
def get_categories():
    return ["All", "Moisturizers", "Cleansers", "Sunscreen", "Serums"]

# Clear the frame before loading new products
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# Main category + product display
def show_category(selected_category, product_frame, products, cart, cart_listbox,
                  total_label, discount_label, tax_label, final_label,
                  discount_var, payment_method, add_to_cart_func):
    
    clear_frame(product_frame)

    # === Top Frame: Category Button + Search Bar ===
    top_frame = tk.Frame(product_frame)
    top_frame.pack(fill=tk.X, pady=5)

    # --- Category Dropdown ---
    category_btn = tk.Menubutton(top_frame, text="☰ Category", relief=tk.RAISED)
    menu = tk.Menu(category_btn, tearoff=0)
    category_btn.config(menu=menu)
    category_btn.pack(side=tk.LEFT, padx=10)

    # Populate menu with all categories
    for cat in get_categories():
        menu.add_command(label=cat, command=lambda c=cat: show_category(
            c, product_frame, products, cart, cart_listbox,
            total_label, discount_label, tax_label, final_label,
            discount_var, payment_method, add_to_cart_func
        ))

    # --- Search Bar ---
    search_var = tk.StringVar()
    search_entry = tk.Entry(top_frame, textvariable=search_var, width=30)
    search_entry.pack(side=tk.LEFT, padx=10)

    # === Scrollable Product Display Area ===
    canvas = tk.Canvas(product_frame)
    scrollbar = tk.Scrollbar(product_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # === Display Filtered Products ===
    def update_display():
        for widget in scrollable_frame.winfo_children():
            widget.destroy()

        filtered = []
        for product in products:
            if selected_category == "All" or product["category"] == selected_category:
                if search_var.get().lower() in product["name"].lower():
                    filtered.append(product)

        columns = 4
        row_frame = None

        for idx, product in enumerate(filtered):
            if idx % columns == 0:
                row_frame = tk.Frame(scrollable_frame)
                row_frame.pack(pady=8)

            frame = tk.Frame(row_frame, bd=2, relief=tk.RIDGE, padx=10, pady=10, width=200, height=260, bg="white")
            frame.pack_propagate(0)
            frame.pack(side=tk.LEFT, padx=12)

            # Load image
            image_path = os.path.join("images", product.get("image", "placeholder.png"))
            if not os.path.exists(image_path):
                image_path = os.path.join("images", "placeholder.png")

            try:
                img = Image.open(image_path).resize((170, 160))
                photo = ImageTk.PhotoImage(img.copy())
            except:
                img = Image.new("RGB", (170, 160), color="gray")
                photo = ImageTk.PhotoImage(img)

            img_label = tk.Label(frame, image=photo, bg="white")
            img_label.image = photo
            img_label.pack()

            # Name and price
            tk.Label(frame, text=product["name"], font=("Arial", 10, "bold"), wraplength=150, bg="white").pack(pady=(5, 2))
            tk.Label(frame, text=f"Rs. {product['price']}", font=("Arial", 9), bg="white").pack()

            # Add to cart on click
            def bind_click(widget, p=product):
                widget.bind("<Button-1>", lambda e: add_to_cart_func(
                    p, cart, cart_listbox, total_label, discount_label, tax_label, final_label,
                    discount_var, payment_method
                ))

            bind_click(frame)
            for child in frame.winfo_children():
                bind_click(child)

    # Search updates product display
    search_var.trace("w", lambda *args: update_display())
    update_display()
