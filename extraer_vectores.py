from deepface import DeepFace
from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import requests

app = Flask(__name__)

BACKEND_URL = "http://127.0.0.1:8000/save_vector"  #esto de ha de adaptar a lo que tengamos !!!!!!!!!!

@app.post("/process")
def process_images():

    data = request.files.getlist("images")

    result = []

    for image in data:
        img = Image.open(image)

        img_array = np.array(img)

        try:
            vector = DeepFace.represent(img_array, model_name ="Facenet", enforce_detection=True) #Si una cara no esta clara (True), deveuelve una lista vacia

            #Si vector no esta vacio (ha podido estraer bien una cara)
            if len(vector) > 0:
                result.append(vector[0]["embedding"])

        except ValueError as e:
            # Si no se detecta una cara
            print(f"Error con {image}: No se detectó cara - {str(e)}")
            continue
        except Exception as e:
            # En caso de cualquier otro error
            print(f"Error procesando {image}: {str(e)}")
            continue

    if not result:
        return jsonify({"error": "No se encontraron vectores"}), 400

    #Convertir la lista de vectores a una matriz para luego hacer el promedio en cada dimension del vector

    result_array = np.array(result)
    result_avg = np.mean(result_array, axis = 0) #aplicamos la media en las filas axis = 0

    response = requests.post(BACKEND_URL, json={"user": user, "vector": result_avg.tolist()})

    if response.status_code == 200:
        return jsonify({"message": f"Vector promedio calculado para {user}"})
    else:
        return jsonify({"error": "Error al enviar el vector promedio al backend"}), 500


# Ejecutamos el servidor Flask
if __name__ == "__main__":
    app.run(debug=True, port=5000)
