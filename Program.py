import tkinter as tk
from tkinter import messagebox

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

def handle_login():
    username = entry_user.get()
    password = entry_pass.get()

    # Validasi login admin (sesuai file asli Anda)
    if username == "admin" and password == "12345":
        messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
        buka_form_registrasi() # Pindah ke form registrasi
    else:
        messagebox.showerror("Login Gagal", "Username atau Password salah!")

root.mainloop()