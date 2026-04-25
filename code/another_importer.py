import os
import json
from random import randint
import django

# Ubah ke projek_uts.settings agar sesuai dengan folder project kamu
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'projek_uts.settings')
django.setup()

from django.contrib.auth.models import User
from core.models import CourseContent, Comment, Course, CourseMember

current_dir = os.path.dirname(os.path.abspath(__file__))
json_files_folder = os.path.join(current_dir, "json-files")

# Load and process course content data
with open(os.path.join(json_files_folder, "contents.json"), 'r') as jsonfile:
    contents = json.load(jsonfile)
    obj_create = []
    for num, content in enumerate(contents):
        if not CourseContent.objects.filter(pk=num+1).exists():
            course_id = Course.objects.filter(pk=int(content['course_id'])).first()
            if course_id:
                obj_create.append(CourseContent(
                    course_id=course_id,
                    video_url=content['video_url'],
                    name=content['name'],
                    description=content['description'],
                    id=num+1
                ))

    CourseContent.objects.bulk_create(obj_create)

# Load and process comments data
with open(os.path.join(json_files_folder, "comments.json"), 'r') as jsonfile:
    comments = json.load(jsonfile)
    obj_create = []
    for num, comment in enumerate(comments):
        course_content = CourseContent.objects.filter(pk=int(comment['content_id'])).first()
        course_member = CourseMember.objects.filter(pk=int(comment['member_id'])).first()
        
        if (course_content) and (course_member) and (not Comment.objects.filter(pk=num+1).exists()):
            obj_create.append(Comment(
                content_id=course_content,
                member_id=course_member,
                comment=comment['comment'],
                id=num+1
            ))

    Comment.objects.bulk_create(obj_create)