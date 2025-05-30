# IA
Dentro de la carpet extraaer_vectores hay el código extraer_vectores.py que consiste en obtener, de las fotografías recibidas, un vector promedio que sea representativo de la persona.

Dentro de la carpeta detectar_usuario hay el código de deteccion.py donde se recibe una fotografía de la cámara IoT, la IA extrae el vector. Si la “face confidence” es mayor al 85% entonces se sabe que hay un rostro en la imagen. Ahora, se ha de determinar si el rostro que aparece está autorizado a entrar. A continuación, se envía al backend el vector obtenido para que busque en la base de datos aquel vector que sea lo más cercano encontrado.
Una vez hecha esta consulta, se envía este vector encontrado a la IA y se compara la distancia que hay entre el vector obtenido de la fotografía recibida de IoT y el vector que se acaba de recibir del Backend (el vector almacenado del usuario).
Si la distancia es mayor a 11, quiere decir que no se ha encontrado este rostro en la base de datos y en consecuencia, la persona no está autorizada a entrar. En cambio, si la distancia es menor a 11, entonces sabemos que se corresponde con la persona encontrada en la base de datos y por lo tanto, está autorizada a entrar. Además, para que la IA aprenda, lo que se hace es ajustar el vector recibido de la base de datos Chroma con el que hemos extraído de la fotografía.

