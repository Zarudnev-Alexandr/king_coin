FROM python:3.9-slim

WORKDIR /app

# Устанавливаем ping
RUN apt-get update && apt-get install -y iputils-ping

# Устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Команда по умолчанию для запуска приложения
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]