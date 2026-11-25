def ubah_pengeluaran(daftar_pengeluaran, indeks, tanggal, kategori, keterangan, nominal):
    if indeks < 0 or indeks >= len(daftar_pengeluaran):
        raise IndexError("Data pengeluaran yang dipilih tidak ditemukan.")

    daftar_pengeluaran[indeks] = {
        "tanggal": tanggal,
        "kategori": kategori,
        "keterangan": keterangan,
        "nominal": int(nominal),
    }