FROM python:3.11

# Устанавливаем зависимости системы
RUN apt-get update && apt-get install -y libpq-dev gcc

# Создаём рабочую директорию
WORKDIR /code

# Копируем requirements.txt и устанавливаем зависимости
COPY requirements.txt /code/
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . /code/
