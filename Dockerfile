FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y curl && \
    pip install --upgrade pip && \
    pip install flask gunicorn argostranslate

WORKDIR /app
COPY . .

EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
