import sqlite3


def connect_to_db():
    conn = sqlite3.connect('db_pasien.db')
    return conn

# buat tabel


def create_db_table():
    try:
        conn = connect_to_db()
        conn.execute('''
        CREATE TABLE IF NOT EXISTS tbl_pasien (
            id_pasien INTEGER PRIMARY KEY NOT NULL,
            nama TEXT NOT NULL,
            jenis_kelamin TEXT NOT NULL,
            penyakit TEXT NOT NULL,
            nama_ruangan TEXT NOT NULL
        );
        ''')
        conn.commit()
        print('Tabel pasien berhasil dibuat')
    except:
        print("Tabel pasien gagal dibuat")
    finally:
        conn.close()

# tambah pasien


def insert_pasien(pasien):
    inserted_pasien = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO tbl_pasien(nama, jenis_kelamin, penyakit, nama_ruangan) VALUES (?, ?, ?, ?)",
                    (pasien['nama'], pasien['jenis_kelamin'], pasien['penyakit'], pasien['nama_ruangan']))
        conn.commit()
        # mendapatkan id pasien yang baru ditambahkan
        inserted_pasien['id'] = cur.lastrowid
        inserted_pasien['nama'] = pasien['nama']
        inserted_pasien['jenis_kelamin'] = pasien['jenis_kelamin']
        inserted_pasien['penyakit'] = pasien['penyakit']
        inserted_pasien['nama_ruangan'] = pasien['nama_ruangan']

    except Exception as e:
        print(f"Error: {e}")
        conn().rollback()
    finally:
        conn.close()
    return inserted_pasien

# get semua pasien


def get_pasiens():
    pasiens = []

    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tbl_pasien")
        rows = cur.fetchall()

        for i in rows:
            pasien = {}
            pasien["id_pasien"] = i["id_pasien"]
            pasien["nama"] = i["nama"]
            pasien["jenis_kelamin"] = i["jenis_kelamin"]
            pasien["penyakit"] = i["penyakit"]
            pasien["nama_ruangan"] = i["nama_ruangan"]
            pasiens.append(pasien)
    except:
        pasiens = []
    return pasiens

# get pasien by id


def get_pasien_by_id(id_pasien):
    pasien = {}
    try:
        conn = connect_to_db()
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cur.execute("SELECT * FROM tbl_pasien WHERE id_pasien = ?", (id_pasien))
        row = cur.fetchone()

        if row is not None:
            pasien["id_pasien"] = row["id_pasien"]
            pasien["nama"] = row["nama"]
            pasien["jenis_kelamin"] = row["jenis_kelamin"]
            pasien["penyakit"] = row["penyakit"]
            pasien["nama_ruangan"] = row["nama_ruangan"]
    except Exception as e:
        print(f"Error: {e}")
    return pasien

# update pasien


def update_pasien(pasien):
    updated_pasien = {}
    try:
        conn = connect_to_db()
        cur = conn.cursor()
        cur.execute("UPDATE tbl_pasien SET nama = ?, jenis_kelamin = ?, penyakit = ?, nama_ruangan = ? WHERE id_pasien = ?",
                    (pasien["nama"], pasien["jenis_kelamin"], pasien["penyakit"], pasien["nama_ruangan"], pasien["id_pasien"],))
        conn.commit()
        updated_pasien = get_pasien_by_id(pasien["id_pasien"])
    except:
        conn.rollback()
        updated_pasien = {}
    finally:
        conn.close()
    return updated_pasien

# hapus pasien


def delete_pasien(id_pasien):
    message = {}
    try:
        conn = connect_to_db()
        conn.execute("DELETE FROM tbl_pasien WHERE id_pasien = ?", (id_pasien))
        conn.commit()
        message["status"] = "Pasien deleted successfully"
    except:
        conn.rollback()
        message["status"] = "Cannot delete pasien"
    finally:
        conn.close()
    return message


# data
if __name__ == '__main__':
    pasiens = []
    pasien1 = {
        "nama": "Anita Ria",
        "jenis_kelamin": "Perempuan",
        "penyakit": "Asam Lambung",
        "nama_ruangan": "Ruangan Mawar"
    }
    pasien2 = {
        "nama": "Ray Arya",
        "jenis_kelamin": "Laki-laki",
        "penyakit": "Radang Paru-Paru",
        "nama_ruangan": "Ruangan Kamboja"
    }
    pasiens.append(pasien1)
    pasiens.append(pasien2)

    create_db_table()

    for i in pasiens:
        print(insert_pasien(i))
