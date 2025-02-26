# Używamy lekkiego obrazu Alpine
FROM python:3.12-alpine

# Ustawiamy katalog roboczy
WORKDIR /app

# Instalujemy zależności systemowe
RUN apk add --no-cache gcc musl-dev libffi-dev

# Kopiujemy zależności Pythona
COPY requirements.txt .

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy backend
COPY server.py .

# Kopiujemy pliki statyczne z frontendu (dist)
COPY frontend/dist/ /app/static/

# Otwieramy port
EXPOSE 5000

# Uruchamiamy serwer Flask z Gunicorn
#CMD ["gunicorn", "-b", "0.0.0.0:5000", "server:app"]
CMD ["python3", "/app/server.py"]
