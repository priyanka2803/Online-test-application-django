from django.shortcuts import render,redirect
from .forms import StudentRegistrationForm,StudentProfileForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import Group,User
from controller import views as c
from .models import Student
from quiz.models import Test,Question,Subject,Option,Score


def save(request):
    userForm=StudentRegistrationForm()
    studentForm=StudentProfileForm()
    mydict={'userForm':userForm,'studentForm':studentForm}
    if request.method=='POST':
        userForm=StudentRegistrationForm(request.POST)
        studentForm=StudentProfileForm(request.POST,request.FILES)
        print("studentForm",studentForm)
        print("Is user valid ",userForm.is_valid())
        print("Is profile valid ",studentForm.is_valid())
        print("Form errors ",userForm.error_messages)
        print("Form non field errors ",userForm.non_field_errors)
        if userForm.is_valid() and studentForm.is_valid():
            print("\nUser is Valid\n")
            password = userForm.cleaned_data.get("password1")
            print("password = ",password)
            user=userForm.save(commit=False)
            user.set_password(password)
            user.is_staff = False
            user.save()
            print("user ",user)
            student=studentForm.save(commit=False)
            student.user=user
            student.save()
            my_student_group = Group.objects.get_or_create(name='STUDENT')
            my_student_group[0].user_set.add(user)
            print("student saved ",student)
        else:
            messages.error(request, userForm.error_messages)
            userForm=StudentRegistrationForm(request.POST)
            studentForm=StudentProfileForm(request.POST,request.FILES)
            return render(request, "student/student_add.html", {"userForm":userForm,"studentForm":studentForm})

        if c.is_teacher(request.user):
            return render(request,'/teacher/dashboard')
        else:
            return redirect('/student/dashboard')
    return render(request,'student/student_add.html',context=mydict)


def create(request):
    userForm=StudentRegistrationForm()
    studentForm=StudentProfileForm()
    return render(request, "student/student_add.html", {"userForm":userForm,"studentForm":studentForm})
    


def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url="/student/login")
@user_passes_test(is_student)
def dashboard(request):
    username=None
    if request.user.is_authenticated:
        username = request.user.username
        tests = Test.objects.all()
        return render(request,'student/dashboard.html',{"username":username,"tests":tests})

@login_required(login_url="/student/login")
@user_passes_test(is_student)
def logout(request):
    return HttpResponseRedirect('/logout/')

@login_required(login_url="/student/login")
@user_passes_test(is_student)
def viewSubjects(request):
    s = Subject.objects.all()
    return render(request,'student/student_viewSubjects.html',{"subjects":s})

@login_required(login_url="/student/login")
@user_passes_test(is_student)
def viewTests(request,id):
    t = Test.objects.filter(subject = Subject.objects.get(id = id)).all()
    print(t)
    return render(request,'student/student_viewTests.html',{"tests":t})

@login_required(login_url="/student/login")
@user_passes_test(is_student)
def viewAllTests(request):
    t = Test.objects.all()
    return render(request,'student/student_viewTests.html',{"tests":t})

@login_required(login_url="/student/login")
@user_passes_test(is_student)
def viewScores(request):
    s = Score.objects.filter(student= Student.objects.get(user=request.user))
    return render(request,'student/student_viewScores.html',{"scores":s})


