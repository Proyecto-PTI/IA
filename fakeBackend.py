from flask import Flask, request, jsonify

app = Flask(__name__)

# Simulamos un almacenamiento de los vectores
user_vectors = {}

@app.post("/save_vector")
def save_vector():
    # Obtenemos los datos JSON enviados desde el servidor de procesamiento de imágenes
    data = request.get_json()

    # Extraemos el vector recibido
    vector = data.get("vector")

    if not vector:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

    # Imprimimos el vector recibido para asegurarnos de que llegó correctamente
    print("Vector recibido en el backend:", vector)

    # Guardamos el vector en un diccionario (simulando la base de datos)
    user_vectors["user_1"] = vector  # Aquí asignamos el vector al 'usuario 1' por ejemplo

    return jsonify({"message": "Vector guardado para el usuario"}), 200






@app.post("/receive_vector")
def receive_vector():
    # Recibimos el vector del usuario para hacer la comparación
    data = request.get_json()

    vector = data.get("vector")

    if not vector:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400


    # Retornamos el vector almacenado para compararlo con el recibido
    return jsonify({"vectorBD": user_vectors["user_1"]}), 200


@app.post("/adjusted_vector")
def adjusted_vector():
    # Recibimos el vector ajustado
    data = request.get_json()

    vector_adjusted = data.get("vectorAdjusted")

    if not vector_adjusted:
        return jsonify({"error": "Faltan datos en la solicitud"}), 400

    # Imprimimos el vector ajustado para asegurarnos de que llegó correctamente
    print("Vector ajustado recibido:", vector_adjusted)

    # Guardamos el vector ajustado (actualizamos el vector del usuario)
    user_vectors["user_1"] = vector_adjusted  # Guardamos el vector ajustado en el backend

    return jsonify({"message": "Vector ajustado guardado para el usuario"}), 200










# Levantamos el servidor del backend
if __name__ == "__main__":
    app.run(debug=True, port=8000)  # Backend corre en el puerto 8000
