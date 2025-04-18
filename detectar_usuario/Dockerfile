# Usamos la imagen de Python
FROM python:3.10-slim

# Establecemos un directorio de trabajo
WORKDIR /usr/src/app

# Instalamos dependencias del sistema necesarias para DeepFace y OpenCV
RUN apt-get update && \
    apt-get install -y build-essential libgl1-mesa-glx libglib2.0-0 && \
    rm -rf /var/lib/apt/lists/*

# Copiamos el archivo requirements.txt 
COPY requirements.txt ./

# Instalamos las dependencias
RUN pip install  --no-cache-dir -r requirements.txt

# Copiamos el en el directorio de trabajo los ficheros
COPY deteccion.py /usr/src/app
COPY ./deepface_local /usr/src/app/deepface_local

RUN pip install ./deepface_local

# Exponemos el puerto 5001 para Flask
EXPOSE 5002

# Ejecutamos el archivo cuando el contenedor se inicie
CMD ["python", "deteccion.py"]

