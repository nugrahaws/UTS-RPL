import tkinter as tk
from tkinter import messagebox
import sqlite3

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect('users_data.db')
    cursor = conn.cursor()

    # Tabel user login
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')

    # Tabel client (data lengkap)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            nim TEXT,
            jurusan TEXT,
            prodi TEXT,
            tanggal_lahir TEXT,
            tempat_tinggal TEXT,
            jenis_kelamin TEXT,
            alamat TEXT
        )
    ''')

    # User default admin
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ("admin", "12345"))
    except:
        pass

    conn.commit()
    conn.close()

# ================= APP =================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Login & Registrasi")
        self.root.geometry("400x550")
        self.show_login()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

    # ================= LOGIN =================
    def show_login(self):
        self.clear()

        tk.Label(self.root, text="LOGIN", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self.root, text="Username").pack()
        self.user = tk.Entry(self.root)
        self.user.pack()

        tk.Label(self.root, text="Password").pack()
        self.pw = tk.Entry(self.root, show="*")
        self.pw.pack()

        tk.Button(self.root, text="Login", command=self.login).pack(pady=10)
        tk.Button(self.root, text="Register Client", command=self.show_register).pack()

    def login(self):
        username = self.user.get()
        password = self.pw.get()

        conn = sqlite3.connect("users_data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",
                       (username, password))
        data = cursor.fetchone()
        conn.close()

        if data:
            messagebox.showinfo("Sukses", "Login berhasil!")
            self.show_admin()
        else:
            messagebox.showerror("Error", "Login gagal!")

    # ================= REGISTER CLIENT =================
    def show_register(self):
        self.clear()

        tk.Label(self.root, text="REGISTRASI CLIENT", font=("Arial", 14)).pack(pady=10)

        fields = [
            "Nama", "NIM", "Jurusan", "Prodi",
            "Tanggal Lahir", "Tempat Tinggal",
            "Jenis Kelamin", "Alamat"
        ]

        self.inputs = {}

        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack(pady=2)
            self.inputs[field] = entry

        tk.Button(self.root, text="Simpan", command=self.save_client).pack(pady=10)
        tk.Button(self.root, text="Kembali", command=self.show_login).pack()

    def save_client(self):
        data = {k: v.get() for k, v in self.inputs.items()}

        if not data["Nama"]:
            messagebox.showwarning("Error", "Nama wajib diisi!")
            return

        conn = sqlite3.connect("users_data.db")
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO clients 
            (nama, nim, jurusan, angkatan, tanggal_lahir, tempat_lahir, jenis_kelamin, alamat)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data["Nama"],
            data["NIM"],
            data["Jurusan"],
            data["Angkatan"],
            data["Tanggal Lahir"],
            data["Tempat Lahir"],
            data["Jenis Kelamin"],
            data["Alamat"]
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Sukses", "Data tersimpan!")
        self.show_login()

    # ================= ADMIN PANEL =================
    def show_admin(self):
        self.clear()

        tk.Label(self.root, text="PANEL ADMIN", font=("Arial", 14)).pack(pady=10)

        listbox = tk.Listbox(self.root, width=60)
        listbox.pack(pady=10)

        conn = sqlite3.connect("users_data.db")
        cursor = conn.cursor()

        cursor.execute("SELECT nama, nim, jurusan, prodi FROM clients")
        data = cursor.fetchall()
        conn.close()

        if data:
            for d in data:
                listbox.insert(tk.END, f"{d[0]} | {d[1]} | {d[2]} | {d[3]}")
        else:
            listbox.insert(tk.END, "Belum ada data")

        tk.Button(self.root, text="Logout", command=self.show_login).pack(pady=10)

# ================= MAIN =================
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
