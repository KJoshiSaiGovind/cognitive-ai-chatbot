from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from nlp import parse
from reasoning import Reasoner
from dialogue_manager import DialogueManager

app = Flask(__name__)
CORS(app)

reasoner = Reasoner()
dm = DialogueManager()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json() or {}
    text = data.get("text", "")
    use_spacy = data.get("use_spacy", False)

    parsed = parse(text, use_spacy=use_spacy)
    result = reasoner.reason(text)
    response = dm.generate_response(parsed, result)

    dm.update_history("user", text)
    dm.update_history("bot", response)

    return jsonify({
        "input": text,
        "parsed": parsed,
        "reasoning": result,
        "response": response,
        "history": list(dm.history)
    })

# if __name__ == "__main__":
#     app.run(debug=True, port=5000)
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
