from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    audio = models.FileField(upload_to=get_audio_upload_path, null=True, blank=True)
    tag = (('Comprehension', 'Comprehension'),('Decision-making','Decision-making'),('Emotional Intelligence','Emotional Intelligence'))
    qtag = models.CharField(max_length=200,choices=tag,null=True,blank=True)

    def __str__(self):
        return f'{self.course.course_name} - {self.question}'


class DecisionMakingQuestion(models.Model):
    ques = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ques.question}'

class EmotionalIntelligenceQuestion(models.Model):
    ques = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ques.question}'
    
class ComprehensionQuestion(models.Model):
    ques = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.ques.question}'
    


@receiver(post_save, sender=Question)
def create_question_tags(sender, instance, created, **kwargs):
    """
    Signal receiver function to create corresponding tag models for a new question.
    """
    if created and instance.qtag == 'Decision-making':
        DecisionMakingQuestion.objects.create(ques=instance)
    elif created and instance.qtag == 'Emotional Intelligence':
        EmotionalIntelligenceQuestion.objects.create(ques=instance)
    elif created and instance.qtag == 'Comprehension':
        ComprehensionQuestion.objects.create(ques=instance)




class Result(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    exam = models.ForeignKey(Course,on_delete=models.CASCADE)
    decision_making_marks = models.PositiveIntegerField(null=True, blank=True)
    emotional_intelligence_marks = models.PositiveIntegerField(null=True, blank=True)
    comprehension_marks = models.PositiveIntegerField(null=True, blank=True)
    marks = models.PositiveIntegerField()
    time_taken_minutes = models.PositiveIntegerField(null=True, blank=True)  # New field to store time taken in minutes
    predict_performance = models.TextField(null=True, blank=True)
    predict_attrition = models.PositiveIntegerField(null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

