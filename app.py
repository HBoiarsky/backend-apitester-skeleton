import pathlib as pl

import numpy as np
import pandas as pd

from flask import Flask, jsonify, request
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

data = pl.Path(__file__).parent.absolute() / 'data'

associations_df = pd.read_csv(data / 'associations_etudiantes.csv')
evenements_df = pd.read_csv(data / 'evenements_associations.csv')

# Vérification serveur actif
@app.route('/api/alive', methods=['GET'])
def alive():
    return jsonify({"message": "Alive"}), 200

# Liste de toutes les associations
@app.route('/api/associations', methods=['GET'])
def get_associations():
    associations = associations_df['id'].tolist()
    return jsonify(associations), 200

# Détails d'une association
@app.route('/api/association/<int:id>', methods=['GET'])
def get_association(id):
    association = associations_df[associations_df['id'] == id]
    if association.empty:
        return jsonify({"error": "Association not found"}), 404
    return jsonify(association.to_dict(orient='records')[0]), 200

# Liste de tous les événements
@app.route('/api/evenements', methods=['GET'])
def get_evenements():
    evenements = evenements_df['id'].tolist()
    return jsonify(evenements), 200

# Détails d'un événement
@app.route('/api/evenement/<int:id>', methods=['GET'])
def get_evenement(id):
    evenement = evenements_df[evenements_df['id'] == id]
    if evenement.empty:
        return jsonify({"error": "Event not found"}), 404
    return jsonify(evenement.to_dict(orient='records')[0]), 200

# Liste des événements d'une association
@app.route('/api/association/<int:id>/evenements', methods=['GET'])
def get_evenements_by_association(id):
    evenements = evenements_df[evenements_df['association_id'] == id]
    return jsonify(evenements.to_dict(orient='records')), 200

# Liste des associations par type
@app.route('/api/associations/type/<type>', methods=['GET'])
def get_associations_by_type(type):
    filtered_associations = associations_df[associations_df['type'] == type]
    return jsonify(filtered_associations.to_dict(orient='records')), 200

if __name__ == '__main__':
    app.run(debug=False)
