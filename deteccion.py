from deepface import DeepFace
import os
import numpy
import requests
import cv2

BACKEND_URL = "http://localhost:5000/receive_vector" #Canviar!!!!!!!!!!!!!!!!!!!


def detect_face():

    capture = cv2.VideoCapture(0);

    while True:

        ok, frame = capture.read() #Devuelve un boleano y la imagen capturada

        if not ok:
            print("No se ha capturado correctamente la imagen")
            break

        #redimendionamos la imagen para que al procesarla sea mucho mas rapido, normalmente los detectores faciales usan de ntre (150x150) a (640x480)
        frame_resize = cv2.resize(frame, (640,480))

        try:
            result = DeepFace.represent(frame_resize, model_name="Facenet", enforce_detection=True)

            if not result
                print("No se ha detectado correctamente la imagen")
                break

            vector = numpy.array(result[0]["emedding"])

            data = {
                "vector": vector.tolist()
            }

            response = request.post(BACKEND_URL, json=data)

        except Exception as e:
            print "Error al procesar la imagen: {str(e)}"

    capture.release()

if __name__ == "__main__":
    detect_face()
