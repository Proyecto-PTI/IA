from deepface import DeepFace
import numpy as np
import requests
import cv2

BACKEND_URL = "http://localhost:8000/receive_vector" #Canviar!!!!!!!!!!!!!!!!!!!
BACKEND2_URL = "http://localhost:8000/adjusted_vector"

THRESHOLD = XXX #SE HA DE PROVAR CUANTO
LEARNING = 0.05 #SE HA DE PROVAR CUANTO pero ha de ser poquito


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

            if not result:
                print("No se ha detectado correctamente la imagen")
                continue

            vector = np.array(result[0]["embedding"])

            data = {
                "vector": vector.tolist()
            }

            response = requests.post(BACKEND_URL, json=data)

            #Respuesta del backend con un vector de la BD  si todo ha ido bien
            if response.status_code == 200:
                data = response.json()

                vectorBD = np.array(data["vectorBD"])   #PONERSE DE ACUERDO CON LOS NOMBRES..........

                #Distancia euclediana entre los dos vectores (siempre sera positivo porque eleva al cuadrado las diferencias)
                dist = np.linalg.norm(vector - vectorBD)

                if dist < THERESHOLD:
                    print("Usuario autorizado a entrar")
                    vectorAdjusted = (1 - LEARNING)*vectorBD + LEARNING*vector

                    adj_data = {
                        "vectorAdjusted": vectorAdjusted.tolist()
                    }

                    adj_resp = requests.post(BACKEND_URL2, json=adj_data)

                    if adj_resp.status_code == 200:
                        print("Vector actualizado enviado correctamente")
                    else:
                        print("Error al actualizar el vector")


                else:
                    print("Usuario no autorizado a entrar")

                    #FALTA DEFINIR QUE QUIERES QUE TE ENVIE CUANDO NO ESTA AUTORIZADO

            else:
                print("Error en la respuesta del backend")


        except Exception as e:
            print ("Error al procesar la imagen")

    capture.release()


if __name__ == "__main__":
    detect_face()
