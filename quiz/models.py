from django.db import models
from teacher.models import Teacher
from student.models import Student

# Create your models here.

class Subject(models.Model):
    subName = models.CharField(max_length=1000)

    def __str__(self):
        return self.subName


class Test(models.Model):
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher,on_delete=models.DO_NOTHING,null=True)
    testTag = models.CharField(max_length=1000,blank=True,null=True)
    testDescription = models.CharField(max_length=1000,blank=True,null=True)

    @property
    def subjectName(self):
        return str(self.subject)

    def __str__(self):
        return str(self.id)+" "+self.subjectName

    
    
    
class Question(models.Model):
    test = models.ForeignKey(Test,on_delete=models.CASCADE)
    qNumber = models.IntegerField()
    question = models.CharField(max_length=1000)
    points = models.IntegerField(default=1)
    correctOption = models.IntegerField()
    def __str__(self):
        return str(self.qNumber)+" "+self.question


class Option(models.Model):
    question = models.ForeignKey(Question,on_delete=models.CASCADE)
    desc = models.CharField(max_length=1000,blank=True,default=" ")
    number = models.IntegerField()

    def __str__(self):
        return str(self.number)+" "+self.desc


class Score(models.Model):
    test = models.ForeignKey(Test,on_delete=models.DO_NOTHING,null=True)
    student = models.ForeignKey(Student,on_delete=models.CASCADE,null=True)
    score = models.IntegerField()
    attempt = models.IntegerField(default=1)

    def __str__(self):
        return str(self.test) + ' ' + str(self.student)


