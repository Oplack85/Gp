FROM python:latest

# تحديث الحزم وتثبيت PostgreSQL و sudo
RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# أمر إضافي (غير ضروري في Dockerfile)
# RUN sudo apt install postgresql postgresql-contrib

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ السكربت الخاص بك
COPY main.py .

# تنفيذ السكربت
CMD ["python", "main.py"]
