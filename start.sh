#!/bin/bash

# تحديث قائمة الحزم
sudo apt-get update

# تثبيت PostgreSQL و PostgreSQL contrib
sudo apt-get install -y postgresql postgresql-contrib
python main.py
echo "successfully. ✔️"
