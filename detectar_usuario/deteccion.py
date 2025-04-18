from deepface import DeepFace
import numpy as np
import requests
import cv2
import sys

# Para no usar la GPU porque da problemas
#import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
#os.environ["TF_CPP_MIN_LOG_LEVEL"] = "2"

BACKEND_URL = "http://localhost:8000/receive_vector"  # Cambiarlo segun los servcios que vayamos a tener
BACKEND2_URL = "http://localhost:8000/adjusted_vector"

THRESHOLD = 10  # TENEMOS QUE HACER TESTEO DE ESTOS VALORES!!!!!!!!!!!!!!!!!!!!!
LEARNING = 0.05

def detect_face(image_path):
    # Cargamos la imagen desde el path
    frame = cv2.imread(image_path)

    if frame is None:
        print(f"Error: No se pudo cargar la imagen desde {image_path}.")
        return

    # Redimensionamos la imagen para que sea más rápido el procesamiento
    frame_resize = cv2.resize(frame, (640, 480))

    try:
        # Usamos DeepFace para obtener el vector de la cara y forzamos a que reconozca una cara
        result = DeepFace.represent(frame_resize, model_name="Facenet", enforce_detection=True)

        if not result:
            print("No se ha detectado correctamente la imagen.")
            return #Acabar de definir esto!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # Obtenemos el vector de la cara
        vector = np.array(result[0]["embedding"])

        # Creamos el payload para enviar al backend
        data = {
            "vector": vector.tolist()
        }

        # Enviamos el vector al backend
        response = requests.post(BACKEND_URL, json=data)

        # Si la respuesta es correcta, calculamos la distancia entre los vectores
        if response.status_code == 200:
            data = response.json()

            # Extraemos el vector almacenado en el backend
            vectorBD = np.array(data["vectorBD"])

            # Calculamos la distancia euclidiana entre los dos vectores
            dist = np.linalg.norm(vector - vectorBD)

            if dist < THRESHOLD:
                print("Usuario autorizado a entrar.")
                # Ajustamos el vector si la distancia es suficiente
                vectorAdjusted = (1 - LEARNING) * vectorBD + LEARNING * vector

                # Enviamos el vector ajustado al backend
                adjusted_data = {
                    "vectorAdjusted": vectorAdjusted.tolist()
                }

                adjusted_response = requests.post(BACKEND2_URL, json=adjusted_data)

                if adjusted_response.status_code == 200:
                    print("Vector ajustado guardado con éxito.")
                else:
                    print("Error al guardar el vector ajustado.")
            else:
                print("Usuario no autorizado a entrar.")
        else:
            print(f"Error en la respuesta del backend. Código de estado: {response.status_code}, Detalles: {response.text}.")
    except Exception as e:
        print(f"Error al procesar la imagen: {str(e)}")

if __name__ == "__main__":
    # Verificamos que se haya pasado el path de la imagen
    if len(sys.argv) < 2:
        print("Por favor, proporciona el path de la imagen.")
        sys.exit(1)

    image_path = sys.argv[1]
    detect_face(image_path)
