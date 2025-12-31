from flask import Flask, request, jsonify, send_file
from MorseEnglishConvertor import MorseEnglishConvertor
import os

app = Flask(__name__)

converter = MorseEnglishConvertor()

@app.route("/eng-to-morse", methods=["POST"])
def eng_to_morse():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    eng_text = data["text"]
    morse_text = converter.eng_to_morse_text(eng_text)

    return jsonify({
        "english": eng_text,
        "morse": morse_text
    })

@app.route("/morse-to-eng", methods=["POST"])
def morse_to_eng():
    data = request.get_json()

    if not data or "morse" not in data:
        return jsonify({"error": "Missing 'morse' field"}), 400

    morse_text = data["morse"]
    eng_text = converter.morse_to_eng_text(morse_text)

    return jsonify({
        "morse": morse_text,
        "english": eng_text
    })

@app.route("/eng-to-morse-audio", methods=["POST"])
def eng_to_morse_audio():
    data = request.get_json()

    if not data or "text" not in data:
        return jsonify({"error": "Missing 'text' field"}), 400

    eng_text = data["text"]
    # output_file = "morse.wav"

    audio_buffer = converter.eng_to_morse_audio(eng_text)

    return send_file(
        audio_buffer,
        mimetype="audio/wav",
        as_attachment=True,
        download_name="morse.wav"
    )

if __name__ == "__main__":
    app.run(debug=False)
