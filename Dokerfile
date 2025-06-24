FROM python:3.10-slim

# Instalar dependencias básicas
RUN apt-get update && \
    apt-get install -y curl && \
    pip install --upgrade pip && \
    pip install flask gunicorn argostranslate

# Establecer carpeta de trabajo
WORKDIR /app

# Copiar la app al contenedor
COPY . .

# Exponer el puerto que usará Flask
EXPOSE 5000

# Arrancar el servidor con Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

