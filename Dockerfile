FROM python:latest

# تحديث الحزم وتثبيت PostgreSQL
RUN apt-get update && apt-get install -y postgresql postgresql-contrib && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ السكربت الخاص بك
WORKDIR /app

COPY main.py /app

CMD ["python", "main.py"]
