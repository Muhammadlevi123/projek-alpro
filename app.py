from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Fungsi untuk membaca file data kasir
def load_data():
    try:
        with open('kasir_data.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

# Fungsi untuk menyimpan data kasir ke file
def save_data(data):
    with open('kasir_data.json', 'w') as f:
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

# Fungsi untuk membaca data dari kasir_data.json
def read_data():
    try:
        with open('kasir_data.json', 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error reading file: {e}")
        return []

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

if __name__ == '__main__':
    app.run(debug=True)
