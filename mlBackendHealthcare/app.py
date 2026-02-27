import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from flask import Flask, request, jsonify
import pickle
import json
import numpy as np
import re
from difflib import SequenceMatcher # Plus précis que get_close_matches pour du sur-mesure

app = Flask(__name__)

# --- 1. CHARGEMENT ---
try:
    model = pickle.load(open('rf_model.pkl', 'rb'))
    encoder = pickle.load(open('encoder.pkl', 'rb'))
    with open('symptoms.json', 'r') as f:
        symptoms_list = json.load(f)
except Exception as e:
    print(f"Erreur : {e}")

# --- 2. LOGIQUE D'INTELLIGENCE NLP ---
def calculer_similarite(a, b):
    """ Calcule un score de 0 à 1 entre deux chaînes de caractères. """
    return SequenceMatcher(None, a, b).ratio()

def extraire_symptomes_intelligent(texte_utilisateur):
    """
    Détecte intelligemment les symptômes sans dictionnaire fixe.
    """
    texte = texte_utilisateur.lower().strip()
    # Nettoyage : on enlève la ponctuation inutile
    texte = re.sub(r'[^\w\s]', '', texte)
    
    symptoms_readable = [s.replace('_', ' ') for s in symptoms_list]
    symptomes_detectes = []
    
    # Stratégie 1 : Recherche de segments (Fenêtre glissante)
    # On teste des groupes de 1, 2 et 3 mots pour matcher avec 'nodal skin eruptions' par exemple
    mots = texte.split()
    segments = []
    for n in range(1, 4): # Unigrams, Bigrams, Trigrams
        for i in range(len(mots) - n + 1):
            segments.append(" ".join(mots[i:i+n]))

    # Stratégie 2 : Comparaison croisée
    for segment in segments:
        for idx, symp_nom in enumerate(symptoms_readable):
            score = calculer_similarite(segment, symp_nom)
            
            # Si la ressemblance est > 85%, on valide le symptôme
            if score > 0.85:
                symptomes_detectes.append(symptoms_list[idx])
            # Cas particulier pour les mots courts (ex: 'fever' vs 'fiver')
            elif len(segment) > 3 and segment in symp_nom:
                symptomes_detectes.append(symptoms_list[idx])
            elif len(segment) > 3 and symp_nom in segment:
                symptomes_detectes.append(symptoms_list[idx])

    return list(set(symptomes_detectes))

# --- 3. PRÉDICTION ---
def faire_diagnostic(symptomes):
    input_vector = np.zeros(len(symptoms_list))
    for s in symptomes:
        if s in symptoms_list:
            input_vector[symptoms_list.index(s)] = 1
            
    probabilites = model.predict_proba([input_vector])[0]
    pred_id = np.argmax(probabilites)
    confiance = probabilites[pred_id] * 100
    
    maladie = encoder.inverse_transform([pred_id])[0]
    return maladie, confiance

# --- 4. ROUTES ---
@app.route('/')
def home():
    return jsonify({"status": "ok", "message": "Healthcare ML API is running"})

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    msg = data.get('message', '')
    print(f"Message reçu : {msg}")
    # Utilisation de la nouvelle fonction intelligente
    extraits = extraire_symptomes_intelligent(msg)
    
    if not extraits:
        return jsonify({"response": "Je n'ai reconnu aucun symptôme. Pouvez-vous reformuler ?"})

    maladie, score = faire_diagnostic(extraits)
    liste_visuelle = ", ".join([s.replace('_', ' ') for s in extraits])
    
    return jsonify({
        "response": f"Symptômes identifiés : <b>{liste_visuelle}</b>.<br>"
                   f"Diagnostic : <b>{maladie}</b> ({score:.2f}% de confiance)."
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False)