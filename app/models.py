# Archivo: app/models.py

import pandas as pd
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from io import BytesIO
from flask import send_file
from flask import make_response
import qrcode
import uuid
from PIL import Image


def cargar_datos():
    try:
        return pd.read_excel('registros.xlsx')
    except FileNotFoundError:
        return pd.DataFrame(columns=['Fecha y Hora', 'marca', 'Nombre','Tipo de documento','Numero de documento', 'ID', 'Estado'])

def guardar_datos(datos):
    # Verificar si hay datos existentes
    if not datos.empty:
        # Actualizar solo las filas que no tienen unaN fecha y hora asignada
        mask_fecha_hora = datos['Fecha y Hora'].isna()
        datos.loc[mask_fecha_hora, 'Fecha y Hora'] = datetime.now()

        # Actualizar solo las filas que no tienen un estado asignado
        mask_estado = datos['Estado'].isna()
        datos.loc[mask_estado, 'Estado'] = True

    # Si no hay datos existentes, agregar uno nuevo con fecha, hora y estado
    else:
        datos = pd.DataFrame(columns=['Fecha y Hora', 'marca', 'Nombre','Tipo de documento',' Numero de documento', 'ID', 'Estado'])
        datos = datos.append({'Fecha y Hora': datetime.now(), 'Estado': True}, ignore_index=True)

    datos['ID'] = [str(uuid.uuid4()) for _ in range(len(datos))]  # Generar un identificador único para cada fila
    
    # Guardar datos actualizados
    datos.to_excel('registros.xlsx', index=False)
    
def generar_pdf(datos):
    pdf_filename = f"credencial.pdf"
    width, height = 8 * cm, 4 * cm
    pdfmetrics.registerFont(TTFont('BebasNeue', 'BebasNeue-Regular.ttf'))
    # Crear el PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=(width, height))
    c.setFont('BebasNeue', 12)
    
    # Crear objeto QR
    qr_data = f"https://www.comicfest.co/"
    qr_object = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=2,
        border=1
    )
    qr_object.add_data(qr_data)
    qr_object.make(fit=True)

    # Crear imagen QR
    img = qr_object.make_image(fill_color="black", back_color="white")
        
    img_buffer = BytesIO()
        
    img.save(img_buffer, format='PNG')
        
    img_buffer.seek(0)
    img_pil = Image.open(img_buffer)
    img_pil.save("qr_image.png")
    
    # Agregar imagen QR al PDF
    c.drawInlineImage(img_pil, 20, 30)

    # Agregar otros datos al PDF
    c.drawString(90, 80, f"{datos['Nombre']}")
    c.drawString(90, 60, f"{datos['Numero de documento']}")
    c.drawString(90, 40, f"{datos['Marca']}")

    c.save()
    
    buffer.seek(0)

    response = make_response(buffer.read())
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline; filename=formulario.pdf'

    return response