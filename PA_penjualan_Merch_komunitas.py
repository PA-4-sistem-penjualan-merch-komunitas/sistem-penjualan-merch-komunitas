import csv
from prettytable import PrettyTable
import pwinput

database_user = "user.csv"
database_produk = "produk.csv"

# cek admin
def cek_admin():
    try:
        with open(database_user, "r") as file:
            baca = csv.reader(file)
            for baris in baca:
                if baris[0] == "admin":
                    return
    except FileNotFoundError:
        pass
    with open(database_user, "w", newline="") as file:
        tulis = csv.writer(file)
        tulis.writerow(["admin", "123", "admin", 0])
# cek produk
def cek_produk():
    try:
        with open(database_produk, "r") as file:
            pass
    except FileNotFoundError:
        with open(database_produk, "w", newline="") as file:
            pass

# buat akun
def buat_akun():
    try:
        print("=== BUAT AKUN USER ===")
        username = input("Masukkan username : ")
        if username.strip() == "":
            print("Username tidak boleh kosong!")
            return
        password = pwinput.pwinput("Masukkan password : ")
        if password.strip() == "":
            print("Username tidak boleh kosong!")
            return
        saldo_awal = 500000
        with open(database_user, "a", newline="") as file:
            tulis = csv.writer(file)
            tulis.writerow([username, password, "user", saldo_awal])
        print("Akun user berhasil dibuat! Saldo awal Rp500.000")
    except KeyboardInterrupt:
        print("Dibatalkan.")

# login
def login():
    try:
        print("=== LOGIN ===")
        username = input("Masukkan username : ")
        password = pwinput.pwinput("Masukkan password : ")
        with open(database_user, "r") as file:
            baca = csv.reader(file)
            for baris in baca:
                if baris[0] == username and baris[1] == password:
                    print("Login berhasil!")
                    return baris
        print("Username atau password salah!")
        return None
    except KeyboardInterrupt:
        print("Login dibatalkan.")
        return None

# tambah produk
def tambah_produk():
    try:
        print("=== TAMBAH PRODUK ===")
        nama = input("Nama produk : ")
        harga = input("Harga produk : ")
        stok = input("Stok produk : ")

        if harga.isdigit() and stok.isdigit() and int(harga) > 0 and int(stok) > 0:
            with open(database_produk, "r") as file:
                data = list(csv.reader(file))
                id_baru = len(data) + 1

            with open(database_produk, "a", newline="") as file:
                tulis = csv.writer(file)
                tulis.writerow([id_baru, nama, harga, stok])
            print(f"Produk ID {id_baru} berhasil ditambahkan!")
        else:
            print("Masukkan angka yang sesuai.")
    except KeyboardInterrupt:
        print("Dibatalkan.")

# tampilkan produk
def tampilkan_produk():
    try:
        print("=== DAFTAR PRODUK ===")
        with open(database_produk, "r") as file:
            baca = csv.reader(file)
            data = [baris for baris in baca if len(baris) == 4]
            if data:
                tabel = PrettyTable(["ID", "Nama Produk", "Harga", "Stok"])
                for baris in data:
                    tabel.add_row([baris[0], baris[1], f"Rp{baris[2]}", baris[3]])
                print(tabel)
            else:
                print("Belum ada produk.")
    except FileNotFoundError:
        print("Belum ada produk.")
    except KeyboardInterrupt:
        print("Kembali ke menu.")

# ubah produk
def ubah_produk():
    try:
        print("=== UBAH PRODUK ===")
        tampilkan_produk()
        id_produk = input("Masukkan ID produk yang ingin diubah: ")

        semua_data = []
        ditemukan = False

        with open(database_produk, "r") as file:
            baca = csv.reader(file)
            for baris in baca:
                if baris[0] == id_produk:
                    nama = input("Nama baru : ")
                    harga = input("Harga baru : ")
                    stok = input("Stok baru : ")
                    if harga.isdigit() and stok.isdigit():
                        semua_data.append([baris[0], nama, harga, stok])
                        ditemukan = True
                    else:
                        print("Masukkan angka yang sesuai.")
                        return
                else:
                    semua_data.append(baris)

        if ditemukan:
            with open(database_produk, "w", newline="") as file:
                tulis = csv.writer(file)
                tulis.writerows(semua_data)
            print("Produk berhasil diubah!")
        else:
            print("Produk tidak ditemukan.")
    except KeyboardInterrupt:
        print("Dibatalkan.")

# hapus produk
def hapus_produk():
    try:
        print("=== HAPUS PRODUK ===")
        tampilkan_produk()
        id_produk = input("Masukkan ID produk yang ingin dihapus: ")

        semua_data = []
        ditemukan = False

        with open(database_produk, "r") as file:
            baca = csv.reader(file)
            for baris in baca:
                if baris[0] == id_produk:
                    ditemukan = True
                else:
                    semua_data.append(baris)

        if ditemukan:
            with open(database_produk, "w", newline="") as file:
                tulis = csv.writer(file)
                tulis.writerows(semua_data)
            print("Produk berhasil dihapus!")
        else:
            print("Produk tidak ditemukan.")
    except KeyboardInterrupt:
        print("Dibatalkan.")

# transaksi
def transaksi(user):
    try:
        print("=== PEMBELIAN PRODUK ===")
        tampilkan_produk()
        id_beli = input("Masukkan ID produk yang ingin dibeli: ")
        jumlah = input("Masukkan jumlah yang ingin dibeli: ")

        if id_beli.isdigit() and jumlah.isdigit() and int(id_beli) > 0 and int(jumlah) > 0:
            semua_data = []
            produk_ada = False
            jumlah = int(jumlah)

            with open(database_produk, "r") as file:
                baca = csv.reader(file)
                for baris in baca:
                    if baris[0] == id_beli:
                        produk_ada = True
                        harga = int(baris[2])
                        stok = int(baris[3])
                        total = harga * jumlah

                        if jumlah > stok:
                            print("Stok tidak cukup!")
                            return

                        saldo = int(user[3])
                        if total > saldo:
                            print("Saldo tidak cukup!")
                            return

                        baris[3] = str(stok - jumlah)
                        semua_data.append(baris)
                        saldo_baru = saldo - total
                        ubah_saldo(user[0], saldo_baru)
                        user[3] = str(saldo_baru)

                        print("\n=== INVOICE ===")
                        print("Nama Pembeli :", user[0])
                        print("Produk       :", baris[1])
                        print("Jumlah       :", jumlah)
                        print("Total Bayar  : Rp", total)
                        print("Sisa Saldo   : Rp", saldo_baru)
                    else:
                        semua_data.append(baris)

            if produk_ada:
                with open(database_produk, "w", newline="") as file:
                    tulis = csv.writer(file)
                    tulis.writerows(semua_data)
            else:
                print("Produk tidak ditemukan.")
        else:
            print("Masukkan angka yang sesuai.")
    except KeyboardInterrupt:
        print("Transaksi dibatalkan.")

# top up saldo
def topup_saldo(user):
    try:
        print("=== TOP UP SALDO ===")
        saldo = int(user[3])
        print("Saldo saat ini: Rp", saldo)
        tambah = input("Masukkan jumlah saldo yang ingin ditambahkan: ")

        if tambah.isdigit() and int(tambah) > 0:
            tambah = int(tambah)
            if saldo + tambah > 1000000:
                print("Gagal! Saldo maksimal Rp1.000.000")
            else:
                saldo_baru = saldo + tambah
                ubah_saldo(user[0], saldo_baru)
                user[3] = str(saldo_baru)
                print("Top up berhasil! Saldo baru: Rp", saldo_baru)
        else:
            print("Masukkan angka yang sesuai.")
    except KeyboardInterrupt:
        print("Top up dibatalkan.")

# ubah saldo
def ubah_saldo(nama_user, saldo_baru):
    semua_user = []
    with open(database_user, "r") as file:
        baca = csv.reader(file)
        for baris in baca:
            if baris[0] == nama_user:
                baris[3] = str(saldo_baru)
            semua_user.append(baris)
    with open(database_user, "w", newline="") as file:
        tulis = csv.writer(file)
        tulis.writerows(semua_user)

# menu utama
cek_admin()
cek_produk()

while True:
    try:
        print("=== MENU UTAMA ===")
        print("1. Buat Akun User")
        print("2. Login")
        print("3. Keluar")
        menu = input("Pilih menu: ")

        if menu == "1":
            buat_akun()
        elif menu == "2":
            user = login()
            if user:
                if user[2] == "admin":
                    while True:
                        print("=== MENU ADMIN ===")
                        print("1. Lihat Produk")
                        print("2. Tambah Produk")
                        print("3. Ubah Produk")
                        print("4. Hapus Produk")
                        print("5. Logout")
                        pilih = input("Pilih menu: ")
                        if pilih == "1":
                            tampilkan_produk()
                        elif pilih == "2":
                            tambah_produk()
                        elif pilih == "3":
                            ubah_produk()
                        elif pilih == "4":
                            hapus_produk()
                        elif pilih == "5":
                            break
                        else:
                            print("Pilihan tidak sesuai.")
                elif user[2] == "user":
                    while True:
                        print("=== MENU USER ===")
                        print("1. Lihat Produk")
                        print("2. Beli Produk")
                        print("3. Top Up Saldo")
                        print("4. Logout")
                        pilih = input("Pilih menu: ")
                        if pilih == "1":
                            tampilkan_produk()
                        elif pilih == "2":
                            transaksi(user)
                        elif pilih == "3":
                            topup_saldo(user)
                        elif pilih == "4":
                            break
                        else:
                            print("Pilihan tidak sesuai.")
        elif menu == "3":
            print("Terima kasih telah menggunakan program!")
            break
        else:
            print("Pilihan tidak sesuai.")
    except (KeyboardInterrupt, EOFError):
        print("Program dihentikan.")

        break
