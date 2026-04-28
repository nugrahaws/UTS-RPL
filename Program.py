import tkinter as tk
from tkinter import messagebox

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()

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

#FUNGSI TAB REGISTRASI

def buka_form_registrasi():
    # Sembunyikan jendela login utama
    root.withdraw()
    
    # Buat jendela baru untuk registrasi
    reg_window = tk.Toplevel()
    reg_window.title("Form Registrasi Client")
    reg_window.geometry("350x500")
    
    # Protokol jika jendela registrasi ditutup (kembali ke login atau keluar semua)
    reg_window.protocol("WM_DELETE_WINDOW", root.destroy)

    def handle_register():
        email = entry_email.get()
        username = entry_user_reg.get()
        password = entry_pass_reg.get()
        address = entry_address.get()
        postcode = entry_postcode.get()

        if not email or not username or not password:
            messagebox.showwarning("Input Error", "Email, Username, dan Password wajib diisi!")
            return

        print(f"Data Terdaftar:\nEmail: {email}\nUser: {username}\nAlamat: {address}\nKodepos: {postcode}")
        messagebox.showinfo("Registrasi Berhasil", f"Akun {username} telah berhasil dibuat!")

    # --- Layout Form Registrasi ---
    tk.Label(reg_window, text="FORM REGISTRASI CLIENT", font=("Arial", 12, "bold")).pack(pady=10)

    tk.Label(reg_window, text="Email (Wajib):").pack(pady=(5, 0))
    entry_email = tk.Entry(reg_window, width=30)
    entry_email.pack(pady=5)

    tk.Label(reg_window, text="Username (Wajib):").pack(pady=(5, 0))
    entry_user_reg = tk.Entry(reg_window, width=30)
    entry_user_reg.pack(pady=5)

    tk.Label(reg_window, text="Password (Wajib):").pack(pady=(5, 0))
    entry_pass_reg = tk.Entry(reg_window, width=30, show="*")
    entry_pass_reg.pack(pady=5)

    tk.Label(reg_window, text="Address (Optional):").pack(pady=(5, 0))
    entry_address = tk.Entry(reg_window, width=30)
    entry_address.pack(pady=5)

    tk.Label(reg_window, text="Postcode (Optional):").pack(pady=(5, 0))
    entry_postcode = tk.Entry(reg_window, width=30)
    entry_postcode.pack(pady=5)

    btn_register = tk.Button(reg_window, text="Daftar Sekarang", command=handle_register, bg="#4CAF50", fg="white", width=20)
    btn_register.pack(pady=25)

root.mainloop()