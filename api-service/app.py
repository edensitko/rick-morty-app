from flask import Flask, jsonify
from scripts.fetch_characters import fetch_characters

app = Flask(__name__)

@app.route('/healthcheck')
def healthcheck():
    return jsonify(status="UP"), 200

@app.route('/characters')
def characters():
    characters = fetch_characters()
    return jsonify(characters), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
