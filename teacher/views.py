from django.shortcuts import render,redirect
from .forms import TeacherRegistrationForm,TeacherProfileForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import Group,User
from django.contrib.auth.decorators import login_required,user_passes_test
from .models import Teacher
from quiz.models import *
from quiz.forms import SubjectForm,TestForm,QuestionForm,OptionForm
from student.models import Student

def save(request):
    userForm=TeacherRegistrationForm()
    teacherForm=TeacherProfileForm()
    mydict={'userForm':userForm,'TeacherForm':teacherForm}
    if request.method=='POST':
        userForm=TeacherRegistrationForm(request.POST)
        teacherForm=TeacherProfileForm(request.POST,request.FILES)
        print("TeacherForm",teacherForm)
        print("Is user valid ",userForm.is_valid())
        print("Is profile valid ",teacherForm.is_valid())
        print("Form errors ",userForm.error_messages)
        print("Form non field errors ",userForm.non_field_errors)
        if userForm.is_valid() and teacherForm.is_valid():
            print("\nUser is Valid\n")
            password = userForm.cleaned_data.get("password1")
            print("password = ",password)
            user=userForm.save(commit=False)
            user.set_password(password)
            user.is_staff = False
            user.save()
            print("user ",user)
            teacher=teacherForm.save(commit=False)
            teacher.user=user
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            print("Teacher saved ",teacher)
        else:
            messages.error(request, userForm.error_messages)
            userForm=TeacherRegistrationForm(request.POST)
            TeacherForm=TeacherProfileForm(request.POST,request.FILES)
            return render(request, "teacher/teacher_add.html", {"userForm":userForm,"teacherForm":TeacherForm})

        return HttpResponseRedirect('/teacher/login')
    return render(request,'teacher/teacher_add.html',context=mydict)


def create(request):
    userForm=TeacherRegistrationForm()
    teacherForm=TeacherProfileForm()
    return render(request, "teacher/teacher_add.html", {"userForm":userForm,"teacherForm":teacherForm})
    


def is_teacher(user):
    if user.groups.filter(name='TEACHER').exists():
        if Teacher.objects.filter(user=user,pending=False).exists():
            return True
        else:
            return False
    else:
        return False


@login_required(login_url="/teacher/login")
@user_passes_test(is_teacher,login_url="/teacher/pending")
def dashboard(request):
    username=None
    if request.user.is_authenticated:
        username = request.user.username
        return render(request,'teacher/dashboard.html',{"username":username})

@login_required(login_url="/teacher/login")
def pending(request):
    if Teacher.objects.get(user=request.user).pending == True:
        return render(request,"teacher/pending.html",{})
    else:
        return redirect("/")

@login_required(login_url="/teacher/login")
@user_passes_test(is_teacher,login_url="/teacher/pending")
def addTest(request):
    subjectForm = SubjectForm()
    testForm = TestForm()
    mydict = {"subjectForm":subjectForm,"testForm":testForm}

    return render(request,'teacher/teacher_addtest.html',mydict)

@login_required(login_url="/teacher/login")
@user_passes_test(is_teacher,login_url="/teacher/pending")
def saveTest(request):
    subjectForm = SubjectForm(request.POST)
    testForm = TestForm(request.POST)
    s = Subject.objects.get_or_create(subName=request.POST.get("subName"))
    sid = int(s[0].id)
    print("Method ",request.method)
    print("Sid ",sid)
    
    mydict = {"subjectForm":subjectForm,"testForm":testForm}
    print("\n\nIn save test")

    if request.method == "POST":
        if subjectForm.is_valid and testForm.is_valid:
            s = Subject.objects.get_or_create(subName=request.POST.get("subName"))
            sid = int(s[0].id)
            print("Subject is submitted")
            t = testForm.save(commit=False)
            t.subject = s[0]
            t.save()
            print("t = ",t)
            request.session["testid"] = t.id
            print("Test is submitted")
            return HttpResponseRedirect("/teacher/addQuestion")
    return render(request,'teacher/teacher_addtest.html',context=mydict)

@login_required(login_url="/teacher/login")
@user_passes_test(is_teacher,login_url="/teacher/pending")
def addQuestion(request):
    questionForm = QuestionForm()
    return render(request,'teacher/teacher_addQuestion.html',{"questionForm":questionForm})

@login_required(login_url="/teacher/login")
@user_passes_test(is_teacher,login_url="/teacher/pending")
def saveQuestion(request):
    questionForm = QuestionForm(request.POST)
    print("Method ",request.method)

    option1 = str(request.POST.get("option1"))
    option2 = str(request.POST.get("option2"))
    option3 = str(request.POST.get("option3"))
    option4 = str(request.POST.get("option4"))
    
    print("option1 =",option1,"!")
    print("option2 =",option2,"!")
    
    mydict = {"questionForm":questionForm}
    print("\n\nIn save test")

    if request.method == "POST":
        if questionForm.is_valid:
            t = Test.objects.get(id = int(request.session["testid"]))
            q = questionForm.save(commit=False)
            q.test = t
            q.save()
            print("Question is submitted")
            q.option_set.create(desc = option1,number=1)
            q.save()
            q.option_set.create(desc = option2,number=2)
            q.save()
            if option3.isspace() == False or option3.isprintable()==False:
                q.option_set.create(desc = option3,number=3)
                q.save()
            if option4.isspace() == False or option4.isprintable()==False:
                q.option_set.create(desc = option4,number=4)
                q.save()
            return HttpResponseRedirect("/teacher/addQuestion")
    return render(request,'teacher/teacher_addQuestion.html',context=mydict)

@login_required(login_url="/teacher/login")
@user_passes_test(is_teacher,login_url="/teacher/pending")
def logout(request):
    return HttpResponseRedirect('/logout/')


@login_required(login_url="/teacher/login")
@user_passes_test(is_teacher,login_url="/teacher/pending")
def viewTest(request,id):
    t = Test.objects.get(id = id)
    return render(request,'teacher/teacher_viewtest.html',{"test":t})


@login_required(login_url="/teacher/login")
@user_passes_test(is_teacher,login_url="/teacher/pending")
def viewTests(request):
    t = Test.objects.all()
    return render(request,'teacher/teacher_viewtests.html',{"tests":t})

@login_required(login_url="/teacher/login")
@user_passes_test(is_teacher,login_url="/teacher/pending")
def viewStudents(request):
    s = Student.objects.all()
    print(s)
    return render(request,'teacher/teacher_viewStudents.html',{"students":s})

@login_required(login_url="/teacher/login")
@user_passes_test(is_teacher,login_url="/teacher/pending")
def viewStudent(request,id):
    s = Student.objects.get(id = id)
    return render(request,'teacher/teacher_viewStudent.html',{"student":s})
    






