from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from .models import Test,Question,Option,Subject,Score
from student.models import Student
from django.contrib.auth.decorators import login_required,user_passes_test
from django.contrib.auth import logout

def home(request):
    return render(request,"quiz/index.html")
def is_student(user):
    return user.groups.filter(name='STUDENT').exists()

@login_required(login_url="/student/login")
@user_passes_test(is_student)
def startTest(request,id):
    print("In start Test")
    t = Test.objects.get(id=id)
    l=[]
    request.session["currentQuestionNumber"]=1
    request.session["testid"]=t.id
    request.session["userAnswers"]=l
    return render(request,'quiz/test.html',{"question":t.question_set.get(qNumber=1)})

@login_required(login_url="/student/login")
@user_passes_test(is_student)
def test(request):
    if request.method == "POST":
        answer = request.POST.get("options")
        print("answer ",answer)
        optionNumber = answer[len(answer)-1]
        print("optionNumber ",optionNumber)
        l = request.session["userAnswers"]
        l.append(optionNumber)
        request.session["userAnswers"] = l
        print(request.session["userAnswers"])
        qNo = request.session["currentQuestionNumber"]
        tid = request.session["testid"]
        t = Test.objects.get(id=tid)
        qNo= qNo+1
        print("qNo = ",qNo,"len = ",len(t.question_set.all()))
        if qNo <= len(t.question_set.all()):
            request.session["currentQuestionNumber"]=qNo
            return render(request,'quiz/test.html',{"question":t.question_set.get(qNumber=qNo)})
        else:
            print("In else answer len ",len(request.session["userAnswers"]))
            return HttpResponseRedirect("/result/")


@login_required(login_url="/student/login")
@user_passes_test(is_student)
def result(request):
    t = Test.objects.get(id = request.session["testid"])
    ans = request.session["userAnswers"]
    ans_score = []
    print("len = ",len(ans))
    print("ans ",ans)
    sum =0
    for i in range(len(ans)):
        print("i = ",i)
        if t.question_set.get(qNumber=(i+1)).correctOption == int(ans[i]):
            score=t.question_set.get(qNumber=(i+1)).points
            tup = (ans[i],t.question_set.get(qNumber=(i+1)).points)
            ans_score.append(tup)
        else:
            print("In else ")
            score=0
            tup = (ans[i],score)
            print("tup = ",tup)
            ans_score.append(tup)
        sum = sum+score
    print(ans_score)
    try:
        a = int( Score.objects.filter(test=t,student=Student.objects.get(user=request.user)).last().attempt)
        a = a+1
    except:
        a=1
    Score.objects.create(test=t,student=Student.objects.get(user=request.user),score=sum,attempt=a)
    return render(request,'student/result.html',{"test":t,"answers":ans_score,"score":sum})



def afterLogout(request):
    logout(request)
    return redirect("/")