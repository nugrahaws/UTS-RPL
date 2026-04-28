import tkinter as tk
from tkinter import messagebox
import sqlite3

def init_db():
    # Menghubungkan ke file database (akan dibuat otomatis jika belum ada)
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()

    # Membuat tabel users
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    # Menambah user default untuk testing (Username: admin, Password: password123)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", 
                       ('admin', 'password123'))
        conn.commit()
        print("Database dan user default berhasil dibuat.")
    except sqlite3.IntegrityError:
        print("User sudah ada.")
    
    conn.close()

if __name__ == "__main__":
    init_db()

# TAB LOGIN ADMIIN
def handle_login():
    username = entry_user.get()
    password = entry_pass.get()

    # Validasi sederhana
    if username == "admin" and password == "12345":
        messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
        buka_form_registrasi()
    else:
        messagebox.showerror("Login Gagal", "Username atau Password salah!")

# Inisialisasi Window
root = tk.Tk()
root.title("Form Login UTS-RPL")
root.geometry("300x200")

# Label & Entry untuk Username
tk.Label(root, text="Username:").pack(pady=5)
entry_user = tk.Entry(root)
entry_user.pack(pady=5)

# Label & Entry untuk Password
tk.Label(root, text="Password:").pack(pady=5)
entry_pass = tk.Entry(root, show="*") # Menggunakan '*' agar password tidak terlihat
entry_pass.pack(pady=5)

# Tombol Login
btn_login = tk.Button(root, text="Login", command=handle_login)
btn_login.pack(pady=20)

root.mainloop()