# Используем стабильную версию python-slim (меньше весит)
FROM python:3.12.10

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем файл с зависимостями
COPY requirements.txt .

# Устанавливаем библиотеки
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код проекта
COPY . .

# Команда для запуска бота
CMD ["python", "main.py"]
