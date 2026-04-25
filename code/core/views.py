from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.core import serializers
from django.db.models import Max, Min, Avg, Count
from core.models import *

# 1. Fungsi Testing (Diperbaiki agar tidak IntegrityError)
def testing(request):
    username_target = "usertesting"
    User.objects.filter(username=username_target).delete()
    
    # List User Sebelum
    users_before = User.objects.all()
    rows_before = "".join([f"<tr><td>{u.id}</td><td>{u.username}</td><td>{u.email}</td></tr>" for u in users_before])
    
    # Proses Testing
    user_test = User.objects.create_user(username=username_target, email="test@uts.com", password="123")
    
    # List User Saat Testing
    users_during = User.objects.all()
    rows_during = "".join([f"<tr><td>{u.id}</td><td>{u.username}</td><td>{u.email}</td></tr>" for u in users_during])
    
    user_test.delete() # Hapus lagi

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; background: #f8f9fa; padding: 20px; }}
            .container {{ display: flex; gap: 20px; justify-content: center; }}
            .box {{ background: white; padding: 15px; border-radius: 10px; box-shadow: 0 5px 15px rgba(0,0,0,0.05); width: 45%; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
            th, td {{ padding: 8px; border-bottom: 1px solid #eee; text-align: left; }}
            th {{ background: #343a40; color: white; }}
            .highlight {{ background: #d4edda; font-weight: bold; }}
            .btn {{ display: inline-block; margin-bottom: 20px; text-decoration: none; color: #007bff; }}
        </style>
    </head>
    <body>
        <a href="/" class="btn">← Kembali</a>
        <h1>🧪 Hasil Run Testing</h1>
        <div class="container">
            <div class="box">
                <h3>Kondisi Awal (Daftar User)</h3>
                <table>
                    <tr><th>ID</th><th>Username</th><th>Email</th></tr>
                    {rows_before}
                </table>
            </div>
            <div class="box">
                <h3>Saat Testing (User Baru Ditambahkan)</h3>
                <table>
                    <tr><th>ID</th><th>Username</th><th>Email</th></tr>
                    {rows_during}
                </table>
                <p style="color: green; font-weight: bold;">* User 'usertesting' berhasil dibuat!</p>
            </div>
        </div>
        <p style="text-align: center; margin-top: 20px; color: #666;">Status: User 'usertesting' telah otomatis dihapus kembali untuk menjaga kebersihan database.</p>
    </body>
    </html>
    """
    return HttpResponse(html)
def allCourse(request):
    courses = Course.objects.all()
    rows = "".join([f"""
        <tr>
            <td>{c.id}</td>
            <td><b>{c.name}</b></td>
            <td>Rp {c.price}</td>
            <td><span class='badge'>{c.teacher.username}</span></td>
        </tr>
    """ for c in courses])

    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; background: #f4f7f6; padding: 40px; }}
            .card {{ background: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
            th {{ background-color: #007bff; color: white; }}
            .badge {{ background: #e1f5fe; color: #01579b; padding: 4px 8px; border-radius: 5px; font-size: 12px; }}
            .btn {{ display: inline-block; margin-bottom: 20px; text-decoration: none; color: #007bff; font-weight: bold; }}
        </style>
    </head>
    <body>
        <div class="card">
            <a href="/" class="btn">← Kembali ke Menu</a>
            <h1>📚 Daftar Mata Kuliah</h1>
            <table>
                <tr><th>ID</th><th>Nama Kursus</th><th>Harga</th><th>Pengajar</th></tr>
                {rows}
            </table>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)

# 3. Fungsi User Courses (Diubah agar Dinamis)
def userCourses(request):
    user_id = request.GET.get('id', 1) 
    try:
        user = User.objects.get(pk=user_id)
        courses = Course.objects.filter(teacher=user)
        
        rows = "".join([f"<tr><td>{c.id}</td><td>{c.name}</td><td>Rp {c.price}</td></tr>" for c in courses])
        if not rows:
            rows = "<tr><td colspan='3' style='text-align:center;'>User ini belum mengajar kursus apapun.</td></tr>"

        html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', sans-serif; background: #f0f2f5; padding: 40px; display: flex; justify-content: center; }}
                .card {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 600px; }}
                .profile-header {{ border-bottom: 2px solid #007bff; padding-bottom: 10px; margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; }}
                th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #eee; }}
                th {{ background: #007bff; color: white; border-radius: 5px 5px 0 0; }}
                .btn {{ display: inline-block; margin-bottom: 15px; text-decoration: none; color: #007bff; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="card">
                <a href="/" class="btn">← Kembali ke Menu</a>
                <div class="profile-header">
                    <h2>👤 Profil Pengajar: {user.username}</h2>
                    <p>Nama Lengkap: <b>{user.first_name} {user.last_name}</b></p>
                </div>
                <h3>📚 Daftar Kursus yang Diajar:</h3>
                <table>
                    <tr><th>ID</th><th>Nama Kursus</th><th>Harga</th></tr>
                    {rows}
                </table>
            </div>
        </body>
        </html>
        """
        return HttpResponse(html)
    except User.DoesNotExist:
        return HttpResponse(f"<h2>User ID {user_id} tidak ditemukan.</h2><a href='/'>Kembali</a>")
# 4. Fungsi Course Stat
def courseStat(request):
    courses = Course.objects.all()
    stats = courses.aggregate(max_price=Max('price'), min_price=Min('price'), avg_price=Avg('price'))
    
    html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; background: #f4f7f6; padding: 40px; display: flex; justify-content: center; }}
            .stat-card {{ background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); width: 500px; }}
            .stat-item {{ display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px dashed #ccc; }}
            .val {{ font-weight: bold; color: #28a745; }}
            .btn {{ display: inline-block; margin-bottom: 20px; text-decoration: none; color: #007bff; }}
        </style>
    </head>
    <body>
        <div class="stat-card">
            <a href="/" class="btn">← Kembali</a>
            <h1>📊 Statistik Kursus</h1>
            <div class="stat-item"><span>Total Kursus:</span> <span class="val">{courses.count()}</span></div>
            <div class="stat-item"><span>Harga Tertinggi:</span> <span class="val">Rp {stats['max_price']}</span></div>
            <div class="stat-item"><span>Harga Terendah:</span> <span class="val">Rp {stats['min_price']}</span></div>
            <div class="stat-item"><span>Rata-rata Harga:</span> <span class="val">Rp {stats['avg_price']}</span></div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html)
# 5. Fungsi Course Detail
def courseDetail(request, course_id):
    try:
        course = Course.objects.annotate(
            m_count=Count('coursemember'),
            cont_count=Count('coursecontent')
        ).get(pk=course_id)
        
        result = {
            "name": course.name,
            "member_count": course.m_count,
            "content_count": course.cont_count
        }
        return JsonResponse(result)
    except Course.DoesNotExist:
        return JsonResponse({"error": "Not found"}, status=404)

# 6. Halaman Menu Utama (Tanpa "User 3")
def index(request):
    html_content = """
    <html>
    <head>
        <title>Menu Navigasi UTS - RGB Mode</title>
        <style>
            /* Animasi Background Bergerak */
            @keyframes gradientBG {
                0% { background-position: 0% 50%; }
                50% { background-position: 100% 50%; }
                100% { background-position: 0% 50%; }
            }

            body { 
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                /* Kombinasi warna RGB yang smooth */
                background: linear-gradient(-45deg, #ee7752, #e73c7e, #23a6d5, #23d5ab);
                background-size: 400% 400%;
                animation: gradientBG 15s ease infinite;
                display: flex; 
                justify-content: center; 
                align-items: center; 
                height: 100vh; 
                margin: 0; 
            }

            .card { 
                background: rgba(255, 255, 255, 0.9); /* Sedikit transparan agar estetik */
                backdrop-filter: blur(10px);
                padding: 2rem; 
                border-radius: 20px; 
                box-shadow: 0 15px 35px rgba(0,0,0,0.2); 
                width: 400px; 
            }

            h1 { text-align: center; color: #1c1e21; margin-bottom: 1.5rem; font-size: 24px; border-bottom: 2px solid #eee; padding-bottom: 10px; }
            ul { list-style: none; padding: 0; }
            li { margin-bottom: 12px; }
            
            a { 
                display: block; 
                padding: 12px; 
                background: #007bff; 
                color: white; 
                text-decoration: none; 
                border-radius: 10px; 
                text-align: center; 
                font-weight: 600; 
                transition: 0.4s; 
            }

            a:hover { 
                background: #0056b3; 
                transform: scale(1.05); 
                box-shadow: 0 5px 15px rgba(0,123,255,0.4);
            }

            .silk-btn { background: #6f42c1; }
            .silk-btn:hover { background: #5a32a3; box-shadow: 0 5px 15px rgba(111,66,193,0.4); }
        </style>
    </head>
    <body>
        <div class="card">
            <h1>PSS </h1>
            <ul>
                <li><a href="/all-course/">📚 Lihat Semua Mata Kuliah</a></li>
                <li><a href="/course-stat/">📊 Statistik Harga & Kursus</a></li>
                <li><a href="/user-courses/?id=1">👤 Kursus Saya</a></li>
                <li><a href="/testing/">🧪 Jalankan Testing</a></li>
                <li><a href="/silk/" class="silk-btn">💜 Dashboard Silk (Monitoring)</a></li>
            </ul>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)