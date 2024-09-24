FROM python:latest
# إعداد مجلد العمل
WORKDIR /app

# نسخ ملف المتطلبات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ السكربت الخاص بك
COPY main.py .

# تنفيذ السكربت
CMD ["python", "main.py"]
