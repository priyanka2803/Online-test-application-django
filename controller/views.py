from django.shortcuts import render,redirect
from teacher.forms import TeacherRegistrationForm,TeacherProfileForm
from student.forms import StudentProfileForm,StudentRegistrationForm
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import Group,User
from django.contrib.auth.decorators import login_required,user_passes_test


from teacher.models import Teacher
from quiz.models import *
from quiz.forms import SubjectForm,TestForm,QuestionForm,OptionForm
from student.models import Student

def is_teacher(user):
    return user.groups.filter(name='TEACHER').exists()

def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

def is_admin(user):
    return user.is_superuser

def afterlogin_view(request):
    if is_student(request.user):      
        return redirect('/student/dashboard')
                
    elif is_teacher(request.user):
        return redirect('/teacher/dashboard')
        
    else:
        return redirect('/ap/dashboard')

def afterlogout_view(request):
    if is_student(request.user):      
        return redirect('/')
                
    elif is_teacher(request.user):
        return redirect('/')
        
    else:
        return redirect('/')


@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
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
            teacher.pending=False
            teacher.save()
            my_teacher_group = Group.objects.get_or_create(name='TEACHER')
            my_teacher_group[0].user_set.add(user)
            print("Teacher saved ",teacher)
        else:
            messages.error(request, userForm.error_messages)
            userForm=TeacherRegistrationForm(request.POST)
            TeacherForm=TeacherProfileForm(request.POST,request.FILES)
            return render(request, "controller/admin_addTeacher.html", {"userForm":userForm,"teacherForm":TeacherForm})

        return HttpResponseRedirect('/ap/dashboard')
    return render(request,'controller/admin_addTeacher.html',context=mydict)

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def create(request):
    userForm=TeacherRegistrationForm()
    teacherForm=TeacherProfileForm()
    return render(request, "controller/admin_addTeacher.html", {"userForm":userForm,"teacherForm":teacherForm})
    

@login_required(login_url="ap/login/")
@user_passes_test(is_admin)
def dashboard(request):
        return render(request,'controller/dashboard.html',{})

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def addTest(request):
    subjectForm = SubjectForm()
    testForm = TestForm()
    mydict = {"subjectForm":subjectForm,"testForm":testForm}

    return render(request,'controller/admin_addtest.html',mydict)

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
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
            return HttpResponseRedirect("/ap/addQuestion")
    return render(request,'controller/admin_addtest.html',context=mydict)

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def addQuestion(request):
    questionForm = QuestionForm()
    return render(request,'controller/admin_addQuestion.html',{"questionForm":questionForm})

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
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
            return HttpResponseRedirect("/ap/addQuestion")
    return render(request,'controller/admin_addQuestion.html',context=mydict)

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def logout(request):
    return HttpResponseRedirect('/logout/')


@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def viewTest(request,id):
    t = Test.objects.get(id = id)
    return render(request,'controller/admin_viewtest.html',{"test":t})


@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def viewTests(request):
    t = Test.objects.all()
    return render(request,'controller/admin_viewtests.html',{"tests":t})

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def viewStudents(request):
    s = Student.objects.all()
    print(s)
    return render(request,'controller/admin_viewStudents.html',{"students":s})

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def viewStudent(request,id):
    s = Student.objects.get(id = id)
    return render(request,'controller/admin_viewStudent.html',{"student":s})


@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def viewTeachers(request):
    t = Teacher.objects.filter(pending=False)
    print(t)
    p = Teacher.objects.filter(pending=True)
    print(p)
    return render(request,'controller/admin_viewTeachers.html',{"teachers":t,"pending":p})

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def viewTeacher(request,id):
    t = Teacher.objects.get(id = id)
    return render(request,'controller/admin_viewTeacher.html',{"teacher":t})

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def pending(request,id):
    if request.POST.get("admit"):
        t = Teacher.objects.get(id=id)
        t.pending=False
        t.save()
        print(Teacher.objects.get(id=id).pending)
    elif request.POST.get("delete"):
        Teacher.objects.get(id=id).delete()
    return redirect('/ap/viewTeachers')

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def saveStudent(request):
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
            return render(request, "controller/student_add.html", {"userForm":userForm,"studentForm":studentForm})

        return redirect('/ap/dashboard')
    return render(request,'controller/student_add.html',context=mydict)

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def addStudent(request):
    userForm=StudentRegistrationForm()
    studentForm=StudentProfileForm()
    return render(request, "controller/student_add.html", {"userForm":userForm,"studentForm":studentForm})

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def saveTeacher(request):
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
            return render(request, "controller/admin_addTeacher.html", {"userForm":userForm,"teacherForm":TeacherForm})

        return HttpResponseRedirect('/ap/dashboard')
    return render(request,'controller/admin_addTeacher.html',context=mydict)

@login_required(login_url="/ap/login")
@user_passes_test(is_admin)
def addTeacher(request):
    userForm=TeacherRegistrationForm()
    studentForm=TeacherProfileForm()
    return render(request, "controller/admin_addTeacher.html", {"userForm":userForm,"teacherForm":studentForm})

  
    







