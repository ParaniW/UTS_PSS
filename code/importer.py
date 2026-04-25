import os
import sys
import django
import csv

# Mengatur path agar script bisa menemukan settings Django
sys.path.append(os.path.abspath(os.path.join(__file__, *[os.pardir] * 3)))

# BAGIAN INI: Ganti 'simplelms.settings' jika folder project utama kamu bernama 'projek_uts'
os.environ['DJANGO_SETTINGS_MODULE'] = 'projek_uts.settings'

django.setup()

from django.contrib.auth.models import User
from core.models import Course, CourseMember

# Tentukan lokasi folder CSV
current_dir = os.path.dirname(os.path.abspath(__file__))
csv_data_folder = os.path.join(current_dir, "csv_data")

# 1. Import User
with open(os.path.join(csv_data_folder, "user-data.csv")) as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):
        if not User.objects.filter(username=row['username']).exists():
            User.objects.create_user(
                id=num+2, 
                username=row['username'],
                password=row['password'],
                email=row['email']
            )

# 2. Import Course
with open(os.path.join(csv_data_folder, "course-data.csv")) as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):
        if not Course.objects.filter(pk=num+1).exists():
            Course.objects.create(
                id=num+1, 
                name=row['name'],
                description=row['description'],
                price=row['price'],
                teacher=User.objects.get(pk=int(row['teacher']))
            )

# 3. Import CourseMember
with open(os.path.join(csv_data_folder, "member-data.csv")) as csvfile:
    reader = csv.DictReader(csvfile)
    for num, row in enumerate(reader):
        if not CourseMember.objects.filter(pk=num+1).exists():
            CourseMember.objects.create(
                id=num+1,
                course_id=Course.objects.get(pk=int(row['course_id'])),
                user_id=User.objects.get(pk=int(row['user_id']))
            )