import os
from flask import Flask, jsonify, request, send_from_directory
from pathlib import Path
import json

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / 'frontend'

app = Flask(__name__, static_folder=str(FRONTEND_DIR), static_url_path='')

# Load KB
KB_PATH = Path(__file__).parent / 'knowledge_base.json'
try:
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        KB = json.load(f)
except Exception:
    KB = {}

SAMPLE_OUTPUT = {
  "Complainant": {
    "Name": "Rajesh Kumar",
    "Father": "Venkat Rao",
    "Age": 34,
    "Community": "Scheduled Caste",
    "Occupation": "Agricultural labourer",
    "Address": "Gollapadu village, Bhimavaram Mandal"
  },
  "DateTime": "14-09-2025, 8:15 PM",
  "Place": "Narsapur Road culvert, Bhimavaram",
  "Accused": [
    {"Name": "Ramesh Babu", "Age": 28, "Relation": "S/o Narayana", "History": "History-sheeter"},
    {"Name": "Srinivas", "Age": 30, "Relation": "Brother-in-law of sarpanch"},
    {"Name": "Murali Krishna", "Age": 32, "Occupation": "Driver", "Address": "Mogaltur"},
    {"Name": "Unknown", "Description": "Medium build, black shirt"}
  ],
  "Vehicles": ["AP-37-BX-4321 (Red Pulsar)", "AP-37-CQ-9187 (Black Splendor)"],
  "WeaponsUsed": ["Country-made pistol", "Stick"],
  "Offences": ["Caste abuse", "Threat with firearm", "Robbery", "Assault causing injury"],
  "Injuries": "Bleeding injury on left arm",
  "PropertyLoss": ["Samsung mobile phone worth ₹15,000", "Cash ₹12,500"],
  "Threats": ["Kill him", "Set fire to his hut"],
  "Witnesses": ["Suresh", "Koteswara Rao", "Lakshmi"],
  "Impact": "Fear, public fled, complainant hospitalized",
  "LegalMapping": {}
}

@app.route('/api/health')
def health():
    return jsonify({"status":"ok"})

@app.route('/api/extract', methods=['POST'])
def extract():
    body = request.get_json(silent=True) or {}
    text = body.get('text','').strip()
    out = dict(SAMPLE_OUTPUT)
    mapping = {}
    for off in out.get('Offences', []):
        mapping[off] = KB.get(off, "Not mapped")
    out['LegalMapping'] = mapping
    out['_input_text'] = text[:1000]
    return jsonify(out)

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path != "" and (FRONTEND_DIR / path).exists():
        return send_from_directory(str(FRONTEND_DIR), path)
    else:
        return send_from_directory(str(FRONTEND_DIR), 'index.html')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)