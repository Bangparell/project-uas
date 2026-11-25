def hapus_pengeluaran(daftar_pengeluaran, indeks):
    if indeks < 0 or indeks >= len(daftar_pengeluaran):
        raise IndexError("Data pengeluaran yang dipilih tidak ditemukan.")

    daftar_pengeluaran.pop(indeks)