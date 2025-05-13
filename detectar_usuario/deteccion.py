from deepface import DeepFace
from flask import Flask, request, jsonify
import numpy as np
import requests
import cv2
import sys

# Para no usar la GPU porque da problemas
#import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
#os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

app = Flask(__name__)

BACKEND_URL = "http://localhost:8000/receive_vector"  # Cambiarlo segun los servcios que vayamos a tener
BACKEND2_URL = "http://localhost:8000/adjusted_vector"

THRESHOLD = 11  # TENEMOS QUE HACER TESTEO DE ESTOS VALORES!!!!!!!!!!!!!!!!!!!!!
LEARNING = 0.05


@app.post("/detect")
def detect_face():

    if 'file' not in request.files:
        return jsonify({"error": "No se encontró el campo file en la solicitud"}), 400

    file = request.files['file']
    try:
        rFile = file.read()
        arr = np.frombuffer(rFile, np.uint8)
        img = cv2.imdecode(arr, cv2.IMREAD_COLOR)

        if img is None:
             print("Decodificar")
             return jsonify({"error": "Error al decodificar la imagen"}), 400


        # Redimensionamos la imagen para que sea más rápido el procesamiento
        frame_resize = cv2.resize(img, (640, 480))


        # Usamos DeepFace para obtener el vector de la cara y forzamos a que reconozca una cara
        result = DeepFace.represent(frame_resize, model_name="Facenet", enforce_detection=False)

        face_confidence = result[0].get("face_confidence", 0)
        print(f"Confianza de detección facial: {face_confidence:.3f}")

        if (face_confidence < 0.85):
            print("No face_confidence");
            return jsonify({"error": "No se ha detectado correctamente la cara"}), 400

        if not result:
            print("No result");
            return jsonify({"error": "No se ha detectado correctamente la cara"}), 400

        # Obtenemos el vector de la cara
        vector = np.array(result[0]["embedding"])

        # Enviamos el vector al backend
        response = requests.post(BACKEND_URL, json={"vector": vector.tolist()})

        # Si la respuesta es correcta, calculamos la distancia entre los vectores
        if response.status_code == 200:
            data = response.json()

            # Extraemos el vector almacenado en el backend
            vectorBD = np.array(data["vectorBD"])

            # Calculamos la distancia euclidiana entre los dos vectores
            dist = np.linalg.norm(vector - vectorBD)

            print(f"Distancia: {dist:.3f}")

            if dist > THRESHOLD:
                print("Usuario no autorizado a entrar.")
                #Si no esta autorizado a entrar devuelvo un vector vacio
                no_authorized_response = requests.post(BACKEND2_URL, json={"vectorAdjusted": []})
            else:
                print("Usuario autorizado a entrar.")
                # Ajustamos el vector si la distancia es suficiente
                vectorAdjusted = (1 - LEARNING) * vectorBD + LEARNING * vector

                # Enviamos el vector ajustado al backend
                adjusted_response = requests.post(BACKEND2_URL, json={"vectorAdjusted": vectorAdjusted.tolist()})

               # if adjusted_response.status_code == 200:
                #    print("Vector ajustado guardado con éxito.")
               # else:
                #    print("Error al guardar el vector ajustado.")
        else:
            return jsonify({"error": "Error al comunicarse con el backend"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({"status": "Proceso completado correctamente"}), 200


if __name__ == "__main__":
    app.run(debug=True, port=5002, host="0.0.0.0")
