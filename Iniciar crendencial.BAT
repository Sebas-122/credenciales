@echo off

cd C:\Users\Lighthouse\Desktop\CREDENCIALES

set FLASK_APP=run.py

echo "Dar Ctrl+Click en la ruta HTTP:"

flask run

start /B flask run
timeout /t 3 /nobreak >nul

start http://127.0.0.1:5000

pause