# Archivo: app/routes.py

from flask import render_template, request, redirect, url_for
from app import app
from app.models import cargar_datos, guardar_datos, generar_pdf
from datetime import datetime
import cv2
from pyzbar.pyzbar import decode

@app.route('/')
def index():
    datos = cargar_datos()
    return render_template('index.html', datos=datos)

@app.route('/registrar', methods=['GET','POST'])
def registrar():
    if request.method == 'POST':
        # Obtener datos del formulario
        marca = request.form.get('marca')
        nombre = request.form.get('nombre')
        Tipo_de_documento = request.form.get('Tipo_de_documento')
        Numero_de_documento = request.form.get('Numero_de_documento')
        Genero = request.form.get('Genero')
        celular = request.form.get('celular')
        Empresa = request.form.get('Empresa')
        Correo = request.form.get('Correo')

        # Cargar datos existentes
        datos = cargar_datos()

        # Agregar nueva fila con fecha y hora exacta
        nueva_fila = {'Fecha y Hora': datetime.now(), 'Marca':marca, 'Nombre': nombre,'Tipo de documento': Tipo_de_documento, 'Numero de documento': Numero_de_documento}
        datos = datos._append(nueva_fila, ignore_index=True)

        # Guardar datos actualizados
        guardar_datos(datos)
        
        # Generar el PDF con los datos del formulario
        return generar_pdf(datos.iloc[-1])  # Tomar la última fila recién agregada

        # Redireccionar a la página principal después de procesar el formulario
        return redirect(url_for('index'))

    return render_template('index.html')
    
@app.route('/escanear_qr')
def escanear_qr():
    # Inicia la cámara
    cap = cv2.VideoCapture(0)

    while True:
        # Lee un cuadro de la cámara
        _, frame = cap.read()

        # Decodifica los códigos QR en el cuadro
        decoded_objects = decode(frame)

        # Dibuja rectángulos alrededor de los códigos QR
        for obj in decoded_objects:
            points = obj.polygon
            if len(points) > 4:
                hull = cv2.convexHull(points)
            else:
                hull = points

            n = len(hull)
            for j in range(n):
                cv2.line(frame, hull[j], hull[(j+1)%n], (0, 255, 0), 3)

        # Muestra el cuadro con los rectángulos
        cv2.imshow("QR Scanner", frame)

        # Espera a que se presione la tecla 'q' para salir
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Libera los recursos y cierra la ventana
    cap.release()
    cv2.destroyAllWindows()

    return "Escaneo de códigos QR finalizado"

if __name__ == '__main__':
    app.run(debug=True)