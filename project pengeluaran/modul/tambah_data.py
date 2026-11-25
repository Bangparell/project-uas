def tambah_pengeluaran(daftar_pengeluaran, tanggal, kategori, keterangan, nominal):
    data_baru = {
        "tanggal": tanggal,
        "kategori": kategori,
        "keterangan": keterangan,
        "nominal": int(nominal),
    }
    daftar_pengeluaran.append(data_baru)