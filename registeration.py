import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from db import connect_db
from admin import show_admin_panel

# LOGIN WINDOW 
def show_login(callback_after_login):
    def login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showwarning("Missing Info", "Please enter username and password.")
            return

        # Hardcoded Admin Login
        if username == "admin" and password == "admin123":
            login_win.destroy()
            show_admin_panel()
            return

        # Check Customer from Database
        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()

    
        if user:
            callback_after_login(login_win)

        else:
            messagebox.showerror("Login Failed", "Invalid credentials.")

    def open_register():
        login_win.withdraw()
        show_register(callback_after_login, login_win)

    login_win = tk.Tk()
    login_win.title("Login Portal")
    login_win.geometry("340x240")
    login_win.configure(bg="#f5f5f5")

    tk.Label(login_win, text="User Login", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

    form_frame = tk.Frame(login_win, bg="#f5f5f5")
    form_frame.pack(pady=10)

    # Username
    tk.Label(form_frame, text="Username:", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    username_entry = tk.Entry(form_frame, width=25)
    username_entry.grid(row=0, column=1, pady=5)

    # Password
    tk.Label(form_frame, text="Password:", font=("Arial", 10), bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    password_entry = tk.Entry(form_frame, width=25, show="*")
    password_entry.grid(row=1, column=1, pady=5)

    # Buttons
    button_frame = tk.Frame(login_win, bg="#f5f5f5")
    button_frame.pack(pady=10)

    login_btn = tk.Button(button_frame, text="Login", bg="#64B160", fg="white", font=("Arial", 10, "bold"), width=12, command=login)
    login_btn.grid(row=0, column=0, padx=10)

    register_btn = tk.Button(button_frame, text="Register", bg="#4797C5", fg="white", font=("Arial", 10, "bold"), width=12, command=open_register)
    register_btn.grid(row=0, column=1, padx=10)

    login_win.mainloop()

# ------------------ REGISTRATION WINDOW ------------------ #
def show_register(callback_after_register, login_window):
    def register_user():
        name = name_entry.get()
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        address = address_entry.get()

        if not name or not username or not password or not email or not address:
            messagebox.showwarning("Missing Info", "Please fill all fields.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
            role = "Customer"  # Only Customer role is allowed
            cursor.execute("INSERT INTO users (name, username, password, email, address, role) VALUES (%s, %s, %s, %s, %s, %s)",
                           (name, username, password, email, address, role))
            conn.commit()
            messagebox.showinfo("Success", "Registration successful.")
            register_win.destroy()
            login_window.deiconify()
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Could not register: {err}")
        finally:
            conn.close()

    def go_back():
        register_win.destroy()
        login_window.deiconify()

    register_win = tk.Toplevel()
    register_win.title("Register")
    register_win.geometry("400x370")
    register_win.configure(bg="#f5f5f5")

    tk.Label(register_win, text="User Registration", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

    form_frame = tk.Frame(register_win, bg="#f5f5f5")
    form_frame.pack(pady=10)

    # Name
    tk.Label(form_frame, text="Name:", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    name_entry = tk.Entry(form_frame, width=30)
    name_entry.grid(row=0, column=1, pady=5)

    # Username
    tk.Label(form_frame, text="Username:", font=("Arial", 10), bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    username_entry = tk.Entry(form_frame, width=30)
    username_entry.grid(row=1, column=1, pady=5)

    # Password
    tk.Label(form_frame, text="Password:", font=("Arial", 10), bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    password_entry = tk.Entry(form_frame, width=30, show="*")
    password_entry.grid(row=2, column=1, pady=5)

    # Email
    tk.Label(form_frame, text="Email:", font=("Arial", 10), bg="#f5f5f5").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    email_entry = tk.Entry(form_frame, width=30)
    email_entry.grid(row=3, column=1, pady=5)

    # Address
    tk.Label(form_frame, text="Address:", font=("Arial", 10), bg="#f5f5f5").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    address_entry = tk.Entry(form_frame, width=30)
    address_entry.grid(row=4, column=1, pady=5)

    # Buttons
    button_frame = tk.Frame(register_win, bg="#f5f5f5")
    button_frame.pack(pady=15)

    register_btn = tk.Button(button_frame, text="Create Account", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15, command=register_user)
    register_btn.grid(row=0, column=0, padx=10)

    back_btn = tk.Button(button_frame, text="← Back", bg="#71aa31", fg="white", font=("Arial", 10, "bold"), width=15, command=go_back)
    back_btn.grid(row=0, column=1, padx=10)
