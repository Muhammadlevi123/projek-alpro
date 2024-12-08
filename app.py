from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

# Nama file untuk menyimpan data kasir
DATA_FILE = 'kasir_data.json'

# Fungsi untuk membaca file data kasir
def load_data():
    if not os.path.exists(DATA_FILE):
        return []  # Kembalikan list kosong jika file belum ada
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []  # Kembalikan list kosong jika file tidak dapat didecode

# Fungsi untuk menyimpan data kasir ke file
def save_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=4)

# Route untuk halaman utama
@app.route('/')
def index():
    return render_template('index.html')

# Route untuk halaman Kasir
@app.route('/kasir')
def kasir():
    data = load_data()
    return render_template('kasir.html', data=data)

# Route untuk menambah data kasir
@app.route('/kasir/add', methods=['POST'])
def add_item():
    nama_barang = request.form['nama_barang']
    harga = request.form['harga']
    jumlah = request.form['jumlah']  # Menangkap jumlah
    new_item = {
        'nama_barang': nama_barang, 
        'harga': int(harga),  # pastikan harga adalah angka
        'jumlah': int(jumlah)   # pastikan jumlah adalah angka integer
    }

    data = load_data()
    data.append(new_item)
    save_data(data)

    return redirect(url_for('kasir'))

# Route untuk menghapus data kasir
@app.route('/kasir/delete/<int:item_id>', methods=['GET'])
def delete_item(item_id):
    data = load_data()
    if 0 <= item_id < len(data):
        data.pop(item_id)
        save_data(data)
    return redirect(url_for('kasir'))

# Route untuk memperbarui data kasir
@app.route('/kasir/update/<int:item_id>', methods=['POST'])
def update_item(item_id):
    data = load_data()
    if 0 <= item_id < len(data):
        # Perbarui data dengan input dari form
        data[item_id]['nama_barang'] = request.form['nama_barang']
        data[item_id]['harga'] = int(request.form['harga'])
        data[item_id]['jumlah'] = int(request.form['jumlah'])
        save_data(data)
    return redirect(url_for('kasir'))


@app.route('/checkout', methods=['POST'])
def checkout():
    nama_barang = request.form['barang']
    jumlah = int(request.form['jumlah'])
    data = load_data()

    # Cari barang berdasarkan nama
    for item in data:
        if item['nama_barang'] == nama_barang:
            total_harga = item['harga'] * jumlah
            return render_template(
                'checkout.html',
                nama_barang=nama_barang,
                harga=item['harga'],
                jumlah=jumlah,
                total_harga=total_harga
            )
    return redirect('/pembelian')  # Kembali ke pembelian jika barang tidak ditemukan

@app.route('/checkout/confirm', methods=['POST'])
def confirm_checkout():
    # Proses konfirmasi pembelian
    return redirect('/')  # Redirect ke halaman utama setelah pembelian


# Route untuk halaman Pembelian Barang
@app.route('/pembelian', methods=['GET', 'POST'])
def pembelian():
    data = load_data()
    if request.method == 'POST':
        nama_barang = request.form['barang']
        jumlah = int(request.form['jumlah'])

        # Cari barang berdasarkan nama
        for item in data:
            if item['nama_barang'] == nama_barang:
                total_harga = item['harga'] * jumlah
                return render_template(
                    'pembelian.html',
                    data=data,
                    success=True,
                    nama_barang=nama_barang,
                    jumlah=jumlah,
                    total_harga=total_harga
                )
        return render_template('pembelian.html', data=data, error="Barang tidak ditemukan.")

    return render_template('pembelian.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)