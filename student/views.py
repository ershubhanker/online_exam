from django.shortcuts import render,redirect,reverse
from . import forms,models
from django.db.models import Sum
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from django.conf import settings
from datetime import date, timedelta
from exam import models as QMODEL
from teacher import models as TMODEL
from datetime import datetime, timedelta
import json
import requests
from django.http import JsonResponse

#for showing signup/login button for student
def studentclick_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'student/studentclick.html')

def student_signup_view(request):
    userForm=forms.StudentUserForm()
    studentForm=forms.StudentForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=forms.StudentUserForm(request.POST)
        studentForm=forms.StudentForm(request.POST,request.FILES)
        if userForm.is_valid() and studentForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
        return HttpResponseRedirect('studentlogin')
    return render(request,'student/studentsignup.html',context=mydict)

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_dashboard_view(request):
    dict={
    
    'total_course':QMODEL.Course.objects.all().count(),
    'total_question':QMODEL.Question.objects.all().count(),
    }
    return render(request,'student/student_dashboard.html',context=dict)

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_exam_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_exam.html',{'courses':courses})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def take_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    total_questions=QMODEL.Question.objects.all().filter(course=course).count()
    questions=QMODEL.Question.objects.all().filter(course=course)
    total_marks=0
    for q in questions:
        total_marks=total_marks + q.marks
    
    return render(request,'student/take_exam.html',{'course':course,'total_questions':total_questions,'total_marks':total_marks})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def start_exam_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    questions=QMODEL.Question.objects.all().filter(course=course)
    if request.method=='POST':
        pass
    else:
        start_time = datetime.now()
        request.session['start_time'] = start_time.isoformat()  # Convert datetime to ISO 8601 format
    response= render(request,'student/start_exam.html',{'course':course,'questions':questions})
    response.set_cookie('course_id',course.id)
    return response


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def calculate_marks_view(request):
    if request.COOKIES.get('course_id') is not None:
        course_id = request.COOKIES.get('course_id')
        course=QMODEL.Course.objects.get(id=course_id)
        start_time_iso = request.session.get('start_time')
        start_time = datetime.fromisoformat(start_time_iso)
        end_time = datetime.now()
        time_taken = (end_time - start_time).seconds // 60
        
        total_marks=0
        dm_marks = 0
        ei_marks = 0
        c_marks = 0
        questions=QMODEL.Question.objects.all().filter(course=course)
        for i, question in enumerate(questions):

            selected_ans = request.COOKIES.get(str(i+1))
            actual_answer = questions[i].answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
            if question.qtag == 'Decision-making' and selected_ans == actual_answer:
                dm_marks += question.marks
            elif question.qtag == 'Emotional Intelligence' and selected_ans == actual_answer:
                ei_marks += question.marks
            elif question.qtag == 'Comprehension' and selected_ans == actual_answer:
                c_marks += question.marks

        # Create a dictionary with the results to send to the API
        api_data = {
            "Comprehension": c_marks,
            "Decision Making": dm_marks,
            "Emotional Intelligence": ei_marks,
            "Time": time_taken
        }

        # Send API request for predicted performance
        performance_response = requests.post('http://127.0.0.1:5000/predict_performance', json=api_data)
        performance_data = performance_response.json()
        predicted_performance = performance_data.get('predictions', [''])[0]

        # Send API request for predicted attrition
        attrition_response = requests.post('http://127.0.0.1:5000/predict_attrition', json=api_data)
        attrition_data = attrition_response.json()
        predicted_attrition = int(attrition_data.get('predictions', [0])[0])

        student = models.Student.objects.get(user_id=request.user.id)
        result = QMODEL.Result()
        result.marks=total_marks
        result.decision_making_marks = dm_marks
        result.emotional_intelligence_marks = ei_marks
        result.comprehension_marks = c_marks
        result.time_taken_minutes = time_taken
        result.predict_performance = predicted_performance
        result.predict_attrition = predicted_attrition
        result.exam=course
        result.student=student
        result.save()

        return HttpResponseRedirect('thankyou')

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def thankyoupage(request):
    return render(request,'student/thankyoupage.html')


@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def view_result_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/view_result.html',{'courses':courses})
    

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def check_marks_view(request,pk):
    course=QMODEL.Course.objects.get(id=pk)
    student = models.Student.objects.get(user_id=request.user.id)
    results= QMODEL.Result.objects.all().filter(exam=course).filter(student=student)
    return render(request,'student/check_marks.html',{'results':results})

@login_required(login_url='studentlogin')
@user_passes_test(is_student)
def student_marks_view(request):
    courses=QMODEL.Course.objects.all()
    return render(request,'student/student_marks.html',{'courses':courses})
  