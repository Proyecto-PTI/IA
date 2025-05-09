from deepface import DeepFace
from flask import Flask, request, jsonify
import numpy as np
from PIL import Image
import requests

app = Flask(__name__)

@app.post("/process")
def process_images():

    data = request.files.getlist("images")

    result = []

    for image in data:
        img = Image.open(image)

        img_array = np.array(img)

        try:

            vector = DeepFace.represent(img_array, model_name ="Facenet", enforce_detection=True) #Si una cara no esta clara (True), deveuelve una lista vacia


            #Si ha podido extraer bien una cara
            if len(vector) > 0:
                result.append(vector[0]["embedding"])

        except ValueError as e:
            # Si no se detecta una cara
            print(f"Error con {image}: No se detectó cara - {str(e)}", end="\n\n")
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

    return jsonify({
        "message": "Vector promedio calculado",
        "vector": result_avg.tolist()
        })


# Ejecutamos el servidor Flask
if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")


