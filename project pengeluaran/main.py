import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk
from modul.tambah_data import tambah_pengeluaran
from modul.ubah_data import ubah_pengeluaran
from modul.hapus_data import hapus_pengeluaran
from modul.hitung_total import format_rupiah, hitung_total_pengeluaran

KATEGORI = ("Makanan & Minuman", "Transportasi", "Belanja", "Tagihan", "Lainnya")  # Tuple
daftar_pengeluaran = []  # List berisi Dictionary transaksi

def isi_teks(kotak_input, teks):
    kotak_input.delete(0, tk.END)
    kotak_input.insert(0, teks)

def buat_input(teks, baris, kolom, opsi=None):
    ttk.Label(frame_form, text=teks).grid(row=baris, column=kolom, sticky="w", pady=4)
    widget = ttk.Combobox(frame_form, values=opsi, state="readonly", width=20) if opsi else ttk.Entry(frame_form, width=22)
    widget.grid(row=baris, column=kolom + 1, padx=6)
    return widget

def reset_form():
    isi_teks(input_tanggal, datetime.now().strftime("%d-%m-%Y"))
    pilih_kategori.set(KATEGORI[0])
    isi_teks(input_keterangan, "")
    isi_teks(input_nominal, "")

def perbarui_layar():
    tabel.delete(*tabel.get_children())
    for i, item in enumerate(daftar_pengeluaran):
        tabel.insert("", "end", iid=str(i), values=(i + 1, item["tanggal"], item["kategori"], item["keterangan"], format_rupiah(item["nominal"])))
    label_total.config(text=f"Total Pengeluaran: {format_rupiah(hitung_total_pengeluaran(daftar_pengeluaran))}")
    reset_form()

def ambil_indeks_terpilih():
    if not tabel.selection():
        raise LookupError("Pilih baris data pada tabel terlebih dahulu.")
    return int(tabel.selection()[0])

# --- AKSI TOMBOL & TABEL ---
def aksi_tambah():
    try:
        tambah_pengeluaran(daftar_pengeluaran, 
                           input_tanggal.get(), 
                           pilih_kategori.get(), 
                           input_keterangan.get(), 
                           input_nominal.get())
        perbarui_layar()
    except ValueError:
        messagebox.showerror("Error", "Nominal harus berupa angka.")

def aksi_ubah():
    try:
        indeks = ambil_indeks_terpilih()
        ubah_pengeluaran(daftar_pengeluaran, indeks, input_tanggal.get(), pilih_kategori.get(), input_keterangan.get(), input_nominal.get())
        perbarui_layar()
    except (LookupError, IndexError) as error:
        messagebox.showerror("Error", str(error))
    except ValueError:
        messagebox.showerror("Error", "Nominal harus berupa angka.")

def aksi_hapus():
    try:
        hapus_pengeluaran(daftar_pengeluaran, ambil_indeks_terpilih())
        perbarui_layar()
    except (LookupError, IndexError) as error:
        messagebox.showerror("Error", str(error))

def saat_baris_diklik(_event):
    if tabel.selection():
        item = daftar_pengeluaran[int(tabel.selection()[0])]
        isi_teks(input_tanggal, item["tanggal"])
        pilih_kategori.set(item["kategori"])
        isi_teks(input_keterangan, item["keterangan"])
        isi_teks(input_nominal, str(item["nominal"]))

# --- SUSUNAN ANTARMUKA GUI ---
app = tk.Tk()
app.title("Pencatatan Pengeluaran Harian")
app.geometry("680x450")
frame_form = ttk.LabelFrame(app, text="Form Pengeluaran", padding=10)
frame_form.pack(fill="x", padx=12, pady=8)
input_tanggal = buat_input("Tanggal (DD-MM-YYYY):", 0, 0)
pilih_kategori = buat_input("Kategori:", 0, 2, KATEGORI)
input_keterangan = buat_input("Keterangan:", 1, 0)
input_nominal = buat_input("Nominal (Rp):", 1, 2)
frame_tombol = ttk.Frame(app)
frame_tombol.pack(pady=4)
for teks, aksi in (("Tambah", aksi_tambah), ("Ubah", aksi_ubah), ("Hapus", aksi_hapus), ("Reset", reset_form)):
    ttk.Button(frame_tombol, text=teks, command=aksi).pack(side="left", padx=5)
kolom = ("No", "Tanggal", "Kategori", "Keterangan", "Nominal")
tabel = ttk.Treeview(app, columns=kolom, show="headings", height=9)
for nama_kolom, lebar in zip(kolom, (40, 100, 140, 230, 130)):
    tabel.heading(nama_kolom, text=nama_kolom)
    tabel.column(nama_kolom, width=lebar)
tabel.pack(fill="both", expand=True, padx=12, pady=6)
tabel.bind("<<TreeviewSelect>>", saat_baris_diklik)
label_total = ttk.Label(app, text="Total Pengeluaran: Rp 0", font=("Segoe UI", 11, "bold"))
label_total.pack(anchor="e", padx=14, pady=(0, 10))
reset_form()
app.mainloop()