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
COPY backend/ .

# Kopiujemy pliki statyczne z frontendu (dist)
COPY frontend/dist/ /app/static/

# Otwieramy port
EXPOSE 8000

# Uruchamiamy serwer Flask z Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:31628", "server:app"]