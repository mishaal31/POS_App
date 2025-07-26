import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector
from db import connect_db
from admin import show_admin_panel

# Main login window
def show_login(callback_after_login):
    def login():
        username = username_entry.get()
        password = password_entry.get()

        if not username or not password:
            messagebox.showwarning("Missing Info", "Please enter username and password.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        query = "SELECT * FROM users WHERE username=%s AND password=%s"
        cursor.execute(query, (username, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            login_win.destroy()
            role = user[6]  # Assuming 5th column is role
            if role == 'Admin':
                show_admin_panel()
            else:
                callback_after_login()
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

# Registration window
def show_register(callback_after_register, login_window):
    def register_user():
        name = name_entry.get()
        username = username_entry.get()
        email = email_entry.get()
        password = password_entry.get()
        address = address_entry.get()
        role = role_var.get()

        if not name or not username or not password or not email or not address or not role:
            messagebox.showwarning("Missing Info", "Please fill all fields.")
            return

        conn = connect_db()
        cursor = conn.cursor()
        try:
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
    register_win.geometry("400x420")
    register_win.configure(bg="#f5f5f5")

    tk.Label(register_win, text="User Registration", font=("Arial", 16, "bold"), bg="#f5f5f5").pack(pady=10)

    form_frame = tk.Frame(register_win, bg="#f5f5f5")
    form_frame.pack(pady=10)

    # Name (new field added at row 0)
    tk.Label(form_frame, text="Name:", font=("Arial", 10), bg="#f5f5f5").grid(row=0, column=0, padx=10, pady=5, sticky="e")
    name_entry = tk.Entry(form_frame, width=30)
    name_entry.grid(row=0, column=1, pady=5)

    # Username (row 1)
    tk.Label(form_frame, text="Username:", font=("Arial", 10), bg="#f5f5f5").grid(row=1, column=0, padx=10, pady=5, sticky="e")
    username_entry = tk.Entry(form_frame, width=30)
    username_entry.grid(row=1, column=1, pady=5)

    # Password (row 2)
    tk.Label(form_frame, text="Password:", font=("Arial", 10), bg="#f5f5f5").grid(row=2, column=0, padx=10, pady=5, sticky="e")
    password_entry = tk.Entry(form_frame, width=30, show="*")
    password_entry.grid(row=2, column=1, pady=5)

    # Email (row 3)
    tk.Label(form_frame, text="Email:", font=("Arial", 10), bg="#f5f5f5").grid(row=3, column=0, padx=10, pady=5, sticky="e")
    email_entry = tk.Entry(form_frame, width=30)
    email_entry.grid(row=3, column=1, pady=5)

    # Address (row 4)
    tk.Label(form_frame, text="Address:", font=("Arial", 10), bg="#f5f5f5").grid(row=4, column=0, padx=10, pady=5, sticky="e")
    address_entry = tk.Entry(form_frame, width=30)
    address_entry.grid(row=4, column=1, pady=5)

    # Role (row 5)
    tk.Label(form_frame, text="Register As:", font=("Arial", 10), bg="#f5f5f5").grid(row=5, column=0, padx=10, pady=5, sticky="e")
    role_var = tk.StringVar()
    role_box = ttk.Combobox(form_frame, textvariable=role_var, values=["Admin", "Staff"], width=27)
    role_box.grid(row=5, column=1, pady=5)

    # Buttons
    button_frame = tk.Frame(register_win, bg="#f5f5f5")
    button_frame.pack(pady=15)

    register_btn = tk.Button(button_frame, text="Create Account", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), width=15, command=register_user)
    register_btn.grid(row=0, column=0, padx=10)

    back_btn = tk.Button(button_frame, text="← Back", bg="#71aa31", fg="white", font=("Arial", 10, "bold"), width=15, command=go_back)
    back_btn.grid(row=0, column=1, padx=10)
