from flask import Flask

app = Flask(__name__)

app.config['EXCEL_FILE'] = 'registros.xlsx'  # Nombre del archivo Excel


from app import routes
