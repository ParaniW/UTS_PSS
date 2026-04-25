from django.contrib import admin
from django.urls import path, include
from core import views # Pastikan ini ada

urlpatterns = [
    path('', views.index), # <--- TAMBAHKAN BARIS INI (Path Kosong)
    path('admin/', admin.site.urls),
    path('silk/', include('silk.urls', namespace='silk')),
    path('testing/', views.testing),
    path('all-course/', views.allCourse),
    path('user-courses/', views.userCourses),
    path('course-stat/', views.courseStat),
    path('course-detail/<int:course_id>/', views.courseDetail),
]