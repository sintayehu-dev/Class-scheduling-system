from django.forms import ModelForm
from .models import *
from django import forms

class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = ['r_number', 'seating_capacity']
        widgets = {
            'r_number': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; height: 40px; display: inline-block; margin:15px;'
            }),
            'seating_capacity': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; height: 40px; display: inline-block; margin:10px; margin-left:30px'
            }),
        }


class InstructorForm(forms.ModelForm):
    class Meta:
        model = Instructor
        fields = ['uid', 'name']
        widgets = {
            'uid': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; display: inline-block; margin:10px;'
            }),
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; display: inline-block; margin:10px; margin-left:30px'
            }),
        }

    def clean_uid(self):
     uid = self.cleaned_data.get('uid')
     if Instructor.objects.filter(uid=uid).exists():
        raise forms.ValidationError("The ID is already used.")
     return uid
    
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if Instructor.objects.filter(name=name).exists():
            raise forms.ValidationError("The name is already used.")
        return name

class MeetingTimeForm(ModelForm):
    class Meta:
        model = MeetingTime
        fields = ['pid', 'time', 'day']
        widgets = {
            'pid': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; height: 40px; display: inline-block; margin-left:28px;'
            }),
            'time': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 60%; height: 40px; display: inline-block; margin-left:80px;',
                'size': 1
            }),
            'day': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 60%; height: 40px; display: inline-block; margin-left:7px;',
                'size': 1
            }),
        }
        labels = {
            "pid": "Meeting ID",
            "time": "Time",
            "day": "Day of the Week"
        }


class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['course_number', 'course_name', 'max_numb_students', 'instructors']
        widgets = {
            'course_number': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; height: 40px; display: inline-block; margin-left:35px;'
            }),
            'course_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; height: 40px; display: inline-block; margin-left:26px;'
            }),
            'max_numb_students': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; height: 40px; display: inline-block; margin-left:10px;'
            }),
            'instructors': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'style': 'width: 60%;  display: inline-block; margin-left:5px;',
                'size': 3
            }),
        }


class DepartmentForm(ModelForm):
    class Meta:
        model = Department
        fields = ['dept_name']
        widgets = {
            'dept_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; display: inline-block; margin-left:10px;'
            }),
        }


class BatchForm(ModelForm):
    class Meta:
        model = Batch
        fields = ['batch_name', 'department', 'courses']
        widgets = {
            'batch_name': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; display: inline-block; margin-left:10px;'
            }),
            'department': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 60%; display: inline-block; margin-left:10px;'
            }),
            'courses': forms.SelectMultiple(attrs={
                'class': 'form-control',
                'style': 'width: 60%; display: inline-block; margin-left:10px;',
                'size': 4
            }),
        }


class SectionForm(ModelForm):
    class Meta:
        model = Section
        fields = ['section_id', 'batch', 'num_class_in_week']
        widgets = {
            'section_id': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; display: inline-block; margin-left:10px;'
            }),
            'batch': forms.Select(attrs={
                'class': 'form-control',
                'style': 'width: 60%; display: inline-block; margin-left:10px;'
            }),
            'num_class_in_week': forms.TextInput(attrs={
                'class': 'form-control',
                'style': 'width: 60%; display: inline-block; margin-left:10px;'
            }),
        }
        
        
class SuggestionForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    suggestion = forms.CharField(widget=forms.Textarea)
    attachment = forms.FileField(required=False)
    
    
from django import forms
from .models import PDF

class PDFUploadForm(forms.ModelForm):
    class Meta:
        model = PDF
        fields = ['title', 'file']
