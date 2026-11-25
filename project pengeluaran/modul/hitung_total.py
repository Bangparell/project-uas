def hitung_total_pengeluaran(daftar_pengeluaran):
    return sum(item["nominal"] for item in daftar_pengeluaran)


def format_rupiah(angka):
    return f"Rp {angka:,}".replace(",", ".")