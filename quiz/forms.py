from django import forms
from django.contrib.auth.models import User
from .models import *

class SubjectForm(forms.ModelForm):
    subName = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Subject Name'}))
    class Meta:
        model = Subject
        fields=["subName"]

class TestForm(forms.ModelForm):
    testTag = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Test Tag','class':'form-control'}),required=False)
    testDescription = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Test Description','class':'form-control'}),required=False)
    class Meta:
        model = Test
        fields=["testTag","testDescription"]

class QuestionForm(forms.ModelForm):
    qNumber = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Question Number','class':'form-control'}))
    question = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Question'}))
    points =  forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Points','class':'form-control'}))
    correctOption = forms.IntegerField(widget=forms.NumberInput(attrs={'placeholder':'Correct Option','class':'form-control'}))
    class Meta:
        model = Question
        fields = ["qNumber","question","points","correctOption"]


class OptionForm(forms.ModelForm):
    desc = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Option Description','value':' '}))
    class Meta:
        model = Option
        fields = ["desc"]
        labels = {
            'Option'
        }