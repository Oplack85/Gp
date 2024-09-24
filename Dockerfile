FROM python:latest

# تحديث الحزم وتثبيت PostgreSQL
RUN apt-get update && apt-get install -y postgresql postgresql-contrib && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ السكربت الخاص بك
COPY start.sh .

# إعطاء الأذونات اللازمة للسكربت
RUN chmod +x start.sh

# الأمر الذي يتم تنفيذه عند تشغيل الحاوية
CMD ["bash", "start.sh"]
