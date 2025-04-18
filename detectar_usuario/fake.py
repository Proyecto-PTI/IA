from flask import Flask, request, jsonify
import numpy as np

app = Flask(__name__)

# Vector de referencia simulado
VECTOR_BD = np.random.rand(128).tolist()

@app.post("/receive_vector")
def receive_vector():
    data = request.get_json()
    print("→ Vector recibido:", data["vector"][:5], "...")  # Mostramos solo los primeros valores
    return jsonify({"vectorBD": VECTOR_BD})

@app.post("/adjusted_vector")
def adjusted_vector():
    data = request.get_json()
    print("→ Vector ajustado:", data["vectorAdjusted"][:5] if data["vectorAdjusted"] else "VACÍO")
    return jsonify({"status": "vector ajustado recibido"}), 200

if __name__ == "__main__":
    app.run(port=8000)
