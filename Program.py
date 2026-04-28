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

def handle_login():
    username = entry_user.get()
    password = entry_pass.get()

    # Validasi sederhana
    if username == "admin" and password == "12345":
        messagebox.showinfo("Login Berhasil", f"Selamat datang, {username}!")
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

import tkinter as tk
from tkinter import messagebox, ttk

# Penyimpanan data sederhana (dalam variabel)
registered_clients = []

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Manajemen Data")
        self.root.geometry("400x500")
        self.show_login_frame()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- FRAME LOGIN ---
    def show_login_frame(self):
        self.clear_frame()
        tk.Label(self.root, text="LOGIN SYSTEM", font=("Arial", 16, "bold")).pack(pady=20)
        
        tk.Label(self.root, text="Email:").pack()
        self.ent_email = tk.Entry(self.root)
        self.ent_email.pack(pady=5)
        
        tk.Label(self.root, text="Password:").pack()
        self.ent_pw = tk.Entry(self.root, show="*")
        self.ent_pw.pack(pady=5)
        
        tk.Button(self.root, text="Login sebagai Admin", width=20, 
                  command=lambda: self.login_process("admin")).pack(pady=10)
        tk.Button(self.root, text="Login sebagai Client", width=20, 
                  command=lambda: self.login_process("client")).pack(pady=5)

    def login_process(self, role):
        email = self.ent_email.get()
        pw = self.ent_pw.get()
        
        # Validasi sederhana (Email & PW tidak boleh kosong)
        if email and pw:
            if role == "admin":
                self.show_admin_panel()
            else:
                self.show_registration_form()
        else:
            messagebox.showwarning("Error", "Silahkan isi email dan password!")

    # --- FRAME REGISTRASI (CLIENT) ---
    def show_registration_form(self):
        self.clear_frame()
        self.root.geometry("450x650")
        tk.Label(self.root, text="FORM REGISTRASI CLIENT", font=("Arial", 14, "bold")).pack(pady=10)
        
        fields = ["Nama", "NIM", "Prodi", "Alamat", "Agama", "Angkatan", "Tempat Tgl Lahir", "Jenis Kelamin"]
        self.inputs = {}

        for field in fields:
            tk.Label(self.root, text=f"{field}:").pack()
            entry = tk.Entry(self.root)
            entry.pack(pady=2)
            self.inputs[field] = entry
            
        tk.Button(self.root, text="Submit Data", bg="green", fg="white", 
                  command=self.save_data).pack(pady=20)
        tk.Button(self.root, text="Logout", command=self.show_login_frame).pack()

    def save_data(self):
        name = self.inputs["Nama"].get()
        if name:
            registered_clients.append(name)
            messagebox.showinfo("Sukses", "Data berhasil dikirim!")
            self.show_login_frame()
        else:
            messagebox.showwarning("Error", "Nama wajib diisi!")

    # --- FRAME ADMIN ---
    def show_admin_panel(self):
        self.clear_frame()
        tk.Label(self.root, text="PANEL ADMIN", font=("Arial", 14, "bold")).pack(pady=10)
        tk.Label(self.root, text="Daftar Client Terdaftar:").pack(pady=5)
        
        listbox = tk.Listbox(self.root, width=40)
        listbox.pack(pady=10)
        
        for client in registered_clients:
            listbox.insert(tk.END, f"  - {client}")
            
        if not registered_clients:
            listbox.insert(tk.END, "Belum ada data.")

        tk.Button(self.root, text="Logout", command=self.show_login_frame).pack(pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()