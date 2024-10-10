import pyotp
import sqlite3
import tkinter as tk
from tkinter import messagebox, ttk
from cryptography.fernet import Fernet  # For encryption
import time

# Generate or load encryption key
def load_key():
    try:
        with open("secret.key", "rb") as key_file:
            return key_file.read()
    except FileNotFoundError:
        key = Fernet.generate_key()
        with open("secret.key", "wb") as key_file:
            key_file.write(key)
        return key

key = load_key()
cipher_suite = Fernet(key)

# Create or connect to database
conn = sqlite3.connect('authguard.db')
c = conn.cursor()

# Create user table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    code_name TEXT PRIMARY KEY,
    your_key TEXT NOT NULL,
    secret TEXT NOT NULL
)
''')
conn.commit()

def generate_secret():
    return pyotp.random_base32()

def save_user(code_name, your_key, secret):
    encrypted_secret = cipher_suite.encrypt(secret.encode()).decode()
    try:
        c.execute("INSERT INTO users (code_name, your_key, secret) VALUES (?, ?, ?)", (code_name, your_key, encrypted_secret))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False

def get_users():
    c.execute("SELECT code_name, secret FROM users")
    return c.fetchall()

def verify_otp(secret, otp):
    totp = pyotp.TOTP(secret)
    return totp.verify(otp)

def decrypt_secret(encrypted_secret):
    return cipher_suite.decrypt(encrypted_secret.encode()).decode()

def register_user():
    code_name = code_name_entry.get()
    your_key = your_key_entry.get()
    
    if not code_name or not your_key:
        messagebox.showerror("Error", "Please enter both code name and your key.")
        return

    secret = generate_secret()
    if save_user(code_name, your_key, secret):
        messagebox.showinfo("Success", f"User registered successfully!\nSecret Key: {secret}")
        load_users()
    else:
        messagebox.showerror("Error", "Code name already exists.")

def load_users():
    for widget in otp_frame.winfo_children():
        widget.destroy()

    users = get_users()
    
    for user in users:
        code_name, encrypted_secret = user
        secret = decrypt_secret(encrypted_secret)
        otp = pyotp.TOTP(secret).now()
        
        # Create a card for each account
        user_frame = tk.Frame(otp_frame, bd=2, relief="groove")
        user_frame.pack(fill="x", pady=5)

        name_label = tk.Label(user_frame, text=code_name, font=("Helvetica", 14))
        name_label.pack(side="left", padx=10)

        otp_label = tk.Label(user_frame, text=otp, font=("Helvetica", 16, "bold"), fg="red")
        otp_label.pack(side="right", padx=10)

        delete_button = ttk.Button(user_frame, text="Delete", command=lambda cn=code_name: delete_user(cn), style="Rounded.Red.TButton")
        delete_button.pack(side="right", padx=5)

        # Update every 30 seconds
        update_otp_label(user_frame, otp_label, secret)

def delete_user(code_name):
    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {code_name}?")
    if confirm:
        c.execute("DELETE FROM users WHERE code_name = ?", (code_name,))
        conn.commit()
        load_users()
        messagebox.showinfo("Deleted", f"{code_name} has been deleted.")

def update_otp_label(frame, otp_label, secret):
    def refresh():
        otp = pyotp.TOTP(secret).now()
        otp_label.config(text=otp)
        frame.after(30000, refresh)
    refresh()

def create_context_menu(entry):
    menu = tk.Menu(entry, tearoff=0)
    menu.add_command(label="Copy", command=lambda: entry.event_generate("<<Copy>>"))    
    menu.add_command(label="Paste", command=lambda: entry.event_generate("<<Paste>>"))

    entry.bind("<Button-3>", lambda event: menu.tk_popup(event.x_root, event.y_root))

# Create GUI
root = tk.Tk()
root.title("AuthGuard")
root.geometry("400x450")

# Set style for ttk widgets
style = ttk.Style()
style.configure("Rounded.TButton", foreground="white", background="#4A90E2", padding=6, relief="flat", font=("Helvetica", 10))
style.configure("Rounded.Red.TButton", foreground="white", background="#E74C3C", padding=6, relief="flat", font=("Helvetica", 10))
style.configure("TButton", font=("Helvetica", 10), borderwidth=0)
style.map("Rounded.TButton", background=[("active", "#3A7DCD")])
style.map("Rounded.Red.TButton", background=[("active", "#D32F2F")])
style.layout("Rounded.TButton", [("Button.padding", {"children": [("Button.label", {"sticky": "nswe"})]})])
style.layout("Rounded.Red.TButton", [("Button.padding", {"children": [("Button.label", {"sticky": "nswe"})]})])

# Main frame
main_frame = tk.Frame(root)
main_frame.pack(fill="both", expand=True)

# Frame inputs for registration
input_frame = tk.Frame(main_frame, bd=2, relief="groove", padx=10, pady=10)
input_frame.pack(fill="x", pady=10)

# Code Name Entry
tk.Label(input_frame, text="Code Name:").grid(row=0, column=0)
code_name_entry = ttk.Entry(input_frame, style="TEntry")
code_name_entry.grid(row=0, column=1, padx=5)
create_context_menu(code_name_entry)

# Your Key Entry
tk.Label(input_frame, text="Your Key:").grid(row=1, column=0)
your_key_entry = ttk.Entry(input_frame, style="TEntry")
your_key_entry.grid(row=1, column=1, padx=5)
create_context_menu(your_key_entry)

# Register Button with Rounded Corners and Blue Background
register_button = ttk.Button(input_frame, text="Add", command=register_user, style="Rounded.TButton")
register_button.grid(row=2, columnspan=2, pady=10, ipadx=50)

# Frame to display users and OTPs
otp_frame = tk.Frame(main_frame)
otp_frame.pack(fill="both", expand=True)

# Load registered users
load_users()

# Run the program
root.mainloop()

# Close the connection to the database
conn.close()