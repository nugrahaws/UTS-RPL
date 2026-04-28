import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import sqlite3
import csv

# --- 1. INISIALISASI DATABASE ---
def init_db():
    conn = sqlite3.connect("database_registrasi.db")
    cursor = conn.cursor()
    # Membuat tabel jika belum ada
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nama TEXT, nim TEXT, prodi TEXT, alamat TEXT, 
            agama TEXT, angkatan TEXT, ttl TEXT, gender TEXT
        )
    ''')
    conn.commit()
    conn.close()

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistem Manajemen Data Terintegrasi")
        self.root.geometry("400x450")
        init_db() # Jalankan database saat aplikasi dimulai
        self.show_login_frame()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # --- 2. FRAME LOGIN ---
    def show_login_frame(self):
        self.clear_frame()
        self.root.geometry("400x450")
        
        tk.Label(self.root, text="LOGIN SYSTEM", font=("Arial", 18, "bold")).pack(pady=30)
        
        tk.Label(self.root, text="Email:", font=("Arial", 10)).pack()
        self.ent_email = tk.Entry(self.root, width=35, font=("Arial", 10))
        self.ent_email.pack(pady=5)
        
        tk.Label(self.root, text="Password:", font=("Arial", 10)).pack()
        self.ent_pw = tk.Entry(self.root, show="*", width=35, font=("Arial", 10))
        self.ent_pw.pack(pady=5)
        
        tk.Button(self.root, text="Login", width=25, height=2, bg="#2196F3", fg="white", 
                  font=("Arial", 10, "bold"), command=self.login_process).pack(pady=30)

    def login_process(self):
        email = self.ent_email.get().strip()
        pw = self.ent_pw.get().strip()
        
        # Logika Login Admin
        if email == "admin@mail.com" and pw == "admin123":
            messagebox.showinfo("Sukses", "Selamat Datang, Admin!")
            self.show_admin_panel()
            
        # Logika Login Client (3 Akun Berbeda)
        elif (email == "client@mail.com" and pw == "client123") or \
             (email == "client1@mail.com" and pw == "client2") or \
             (email == "client2@mail.com" and pw == "client3"):
            messagebox.showinfo("Sukses", f"Login Berhasil: {email}")
            self.show_registration_form()
            
        else:
            messagebox.showerror("Error", "Email atau Password Salah!")

    # --- 3. FRAME REGISTRASI CLIENT ---
    def show_registration_form(self):
        self.clear_frame()
        self.root.geometry("750x800")
        
        tk.Label(self.root, text="FORM REGISTRASI CLIENT", font=("Arial", 18, "bold")).pack(pady=30)
        
        form_container = tk.Frame(self.root)
        form_container.pack(pady=10, padx=50)

        fields = ["Nama", "NIM", "Prodi", "Alamat", "Agama", "Angkatan", "Tempat Tgl Lahir", "Jenis Kelamin"]
        self.inputs = {}
        font_style = ("Arial", 12)

        for i, field in enumerate(fields):
            tk.Label(form_container, text=f"{field}:", font=font_style, width=20, anchor="w").grid(row=i, column=0, pady=10)
            entry = tk.Entry(form_container, width=45, font=font_style, bd=2)
            entry.grid(row=i, column=1, pady=10)
            self.inputs[field] = entry
            
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=40)
        
        tk.Button(btn_frame, text="Submit Data", bg="#4CAF50", fg="white", width=18, height=2,
                  font=("Arial", 10, "bold"), command=self.save_to_db).pack(side="left", padx=15)
        
        tk.Button(btn_frame, text="Logout", bg="#f44336", fg="white", width=18, height=2,
                  font=("Arial", 10, "bold"), command=self.show_login_frame).pack(side="left", padx=15)

    def save_to_db(self):
        d = {k: v.get() for k, v in self.inputs.items()}
        if d["Nama"] and d["NIM"]:
            try:
                conn = sqlite3.connect("database_registrasi.db")
                cursor = conn.cursor()
                cursor.execute('''INSERT INTO clients (nama, nim, prodi, alamat, agama, angkatan, ttl, gender) 
                                  VALUES (?,?,?,?,?,?,?,?)''', 
                               (d["Nama"], d["NIM"], d["Prodi"], d["Alamat"], d["Agama"], 
                                d["Angkatan"], d["Tempat Tgl Lahir"], d["Jenis Kelamin"]))
                conn.commit()
                conn.close()
                messagebox.showinfo("Berhasil", "Data Anda telah disimpan ke Database!")
                self.show_login_frame()
            except Exception as e:
                messagebox.showerror("DB Error", f"Terjadi kesalahan: {e}")
        else:
            messagebox.showwarning("Peringatan", "Nama dan NIM wajib diisi!")

    # --- 4. PANEL ADMIN ---
    def show_admin_panel(self):
        self.clear_frame()
        self.root.geometry("1100x650")
        
        tk.Label(self.root, text="PANEL DATABASE ADMIN", font=("Arial", 16, "bold")).pack(pady=20)

        # Container Tabel
        table_frame = tk.Frame(self.root)
        table_frame.pack(pady=10, padx=20, fill="both", expand=True)

        cols = ("Nama", "NIM", "Prodi", "Alamat", "Agama", "Angkatan", "TTL", "Gender")
        tree = ttk.Treeview(table_frame, columns=cols, show='headings', height=12)
        
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")

        # Load Data dari SQLite
        conn = sqlite3.connect("database_registrasi.db")
        cursor = conn.cursor()
        cursor.execute("SELECT nama, nim, prodi, alamat, agama, angkatan, ttl, gender FROM clients")
        for row in cursor.fetchall():
            tree.insert("", tk.END, values=row)
        conn.close()

        # Scrollbar Vertikal & Horizontal
        sy = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
        sx = ttk.Scrollbar(table_frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=sy.set, xscrollcommand=sx.set)
        
        sy.pack(side="right", fill="y")
        sx.pack(side="bottom", fill="x")
        tree.pack(side="left", fill="both", expand=True)

        # Tombol Aksi
        btn_admin_container = tk.Frame(self.root)
        btn_admin_container.pack(side="bottom", pady=30)

        tk.Button(btn_admin_container, text="Download CSV", bg="#2196F3", fg="white", 
                  width=25, height=2, font=("Arial", 10, "bold"), command=self.download_csv).pack(side="left", padx=10)

        tk.Button(btn_admin_container, text="Logout", bg="#f44336", fg="white", 
                  width=25, height=2, font=("Arial", 10, "bold"), command=self.show_login_frame).pack(side="left", padx=10)

    def download_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            conn = sqlite3.connect("database_registrasi.db")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clients")
            rows = cursor.fetchall()
            headers = [d[0] for d in cursor.description]
            
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(headers)
                writer.writerows(rows)
            conn.close()
            messagebox.showinfo("Info", "Data berhasil diekspor ke CSV!")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()