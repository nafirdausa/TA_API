from Data import *
from flask import Flask, request, jsonify
from flask_basicauth import BasicAuth


app = Flask(__name__)

app.config['BASIC_AUTH_USERNAME'] = 'admin'
app.config['BASIC_AUTH_PASSWORD'] = 'admin123'
basic_auth = BasicAuth(app)

#============== RESOURCE ============#

# resource get semua pasien


@app.route('/pasien', methods=['GET'])
@basic_auth.required
def pasien():
    pasiens = get_pasiens()
    if pasiens:
        return jsonify(pasiens), 200  # Sukses dengan kode status 200
    else:
        return jsonify({'message': 'No users found.'}), 404

# resource get pasien by id


@app.route('/pasien/<id_pasien>', methods=['GET'])
@basic_auth.required
def get_pasiens_by_id(id_pasien):
    return jsonify(get_pasien_by_id(id_pasien))

# resource tambah pasien


@app.route('/pasien', methods=['POST'])
@basic_auth.required
def add_pasiens():
    pasien = request.get_json()
    return jsonify(insert_pasien(pasien))

# resource update pasien


@app.route('/pasien', methods=['PUT'])
@basic_auth.required
def update_pasiens():
    pasien = request.get_json()
    return jsonify(update_pasien(pasien))

# resource delete pasien by id


@app.route('/pasien/<id_pasien>', methods=['DELETE'])
@basic_auth.required
def delete_pasiens(id_pasien):
    return jsonify(delete_pasien(id_pasien))


