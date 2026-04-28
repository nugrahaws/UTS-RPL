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

    # Tabel client (Sudah disesuaikan: angkatan & tempat_lahir)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT,
            nim TEXT,
            jurusan TEXT,
            angkatan TEXT,
            tanggal_lahir TEXT,
            tempat_lahir TEXT,
            jenis_kelamin TEXT,
            alamat TEXT
        )
    ''')

    # User default admin
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       ("admin", "12345"))
    except sqlite3.IntegrityError:
        pass

    conn.commit()
    conn.close()

# ================= APP =================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Login & Registrasi")
        self.root.geometry("400x600")
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

        tk.Button(self.root, text="Login", command=self.login, bg="blue", fg="white", width=15).pack(pady=10)
        tk.Button(self.root, text="Register Client", command=self.show_register, width=15).pack()

    def login(self):
        username = self.user.get()
        password = self.pw.get()

        conn = sqlite3.connect("users_data.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        data = cursor.fetchone()
        conn.close()

        if data:
            messagebox.showinfo("Sukses", "Login berhasil!")
            self.show_admin()
        else:
            messagebox.showerror("Error", "Username atau Password salah!")

    # ================= REGISTER CLIENT =================
    def show_register(self):
        self.clear()
        tk.Label(self.root, text="REGISTRASI CLIENT", font=("Arial", 14, "bold")).pack(pady=10)

        # Label field disesuaikan permintaan
        fields = [
            "Nama", "NIM", "Jurusan", "Angkatan",
            "Tanggal Lahir", "Tempat Lahir",
            "Jenis Kelamin", "Alamat"
        ]

        self.inputs = {}
        for field in fields:
            tk.Label(self.root, text=field).pack()
            entry = tk.Entry(self.root)
            entry.pack(pady=2)
            self.inputs[field] = entry

        tk.Button(self.root, text="Simpan", command=self.save_client, bg="green", fg="white", width=15).pack(pady=10)
        tk.Button(self.root, text="Kembali", command=self.show_login, width=15).pack()

    def save_client(self):
        # Ambil data dari input
        data = {k: v.get() for k, v in self.inputs.items()}

        if not data["Nama"] or not data["NIM"]:
            messagebox.showwarning("Error", "Nama dan NIM wajib diisi!")
            return

        try:
            conn = sqlite3.connect("users_data.db")
            cursor = conn.cursor()

            # Query Insert disesuaikan dengan struktur tabel terbaru
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
            messagebox.showinfo("Sukses", "Data client berhasil disimpan!")
            self.show_login()
        except Exception as e:
            messagebox.showerror("Error Database", f"Terjadi kesalahan: {e}")

    # ================= ADMIN PANEL =================
    def show_admin(self):
        self.clear()
        tk.Label(self.root, text="PANEL ADMIN (DATA CLIENT)", font=("Arial", 14, "bold")).pack(pady=10)

        # Listbox untuk menampilkan data
        listbox = tk.Listbox(self.root, width=50, height=15)
        listbox.pack(pady=10)

        conn = sqlite3.connect("users_data.db")
        cursor = conn.cursor()
        # Query SELECT disesuaikan (angkatan)
        cursor.execute("SELECT nama, nim, angkatan FROM clients")
        rows = cursor.fetchall()
        conn.close()

        if rows:
            for r in rows:
                listbox.insert(tk.END, f"{r[1]} - {r[0]} ({r[2]})")
        else:
            listbox.insert(tk.END, "Belum ada data client.")

        tk.Button(self.root, text="Logout", command=self.show_login, bg="red", fg="white").pack(pady=10)

# ================= MAIN =================
if __name__ == "__main__":
    init_db()
    root = tk.Tk()
    app = App(root)
    root.mainloop()
