from django.db import models
import os
from django.utils import timezone

from student.models import Student

def get_audio_upload_path(instance, filename):
    filename = timezone.now().strftime('%Y%m%d%H%M%S') + os.path.splitext(filename)[1]
    return os.path.join('audio/', filename)

class Course(models.Model):
   TIMER_CHOICES = (
        (30, '30 minutes'),
        (45, '45 minutes'),
        (60, '60 minutes'),
        (90, '90 minutes'),
    )
   course_name = models.CharField(max_length=50)
   question_number = models.PositiveIntegerField()
   total_marks = models.PositiveIntegerField()
   audio = models.FileField(upload_to=get_audio_upload_path, null=True, blank=True)
   timer = models.IntegerField(choices=TIMER_CHOICES, null=True, blank=True)

   def __str__(self):
        return self.course_name

class Question(models.Model):
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    qt = (('Fill in the blanks','Fill in the blanks'),('MCQ','MCQ'))
    qtype = models.CharField(max_length=100,null=True, blank=True,choices=qt)
    marks=models.PositiveIntegerField()
    question=models.CharField(max_length=600)
    option1=models.CharField(max_length=200,null=True, blank=True)
    option2=models.CharField(max_length=200,null=True, blank=True)
    option3=models.CharField(max_length=200,null=True, blank=True)
    option4=models.CharField(max_length=200,null=True, blank=True)
    cat=(('Option1','Option1'),('Option2','Option2'),('Option3','Option3'),('Option4','Option4'))
    answer=models.CharField(max_length=200,choices=cat)
    blankans = models.CharField(max_length=100, null=True, blank=True)

class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    marks = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now=True)

