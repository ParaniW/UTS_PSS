from django.contrib import admin
from .models import Course, CourseMember, CourseContent, Comment

# Daftarkan model agar muncul di Admin Panel
admin.site.register(Course)
admin.site.register(CourseMember)
admin.site.register(CourseContent)
admin.site.register(Comment)