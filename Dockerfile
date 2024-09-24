FROM python:latest

# تحديث الحزم وتثبيت PostgreSQL و sudo
RUN apt-get update && \
    apt-get install -y postgresql postgresql-contrib sudo && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# إعداد مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ السكربت الخاص بك
COPY main.py .

# تغيير المستخدم إلى الجذر
USER root

# تنفيذ السكربت
CMD ["python", "main.py"]
