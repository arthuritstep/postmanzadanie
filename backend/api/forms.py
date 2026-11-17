from django import forms
from .models import Attendance, Lesson, User


class LessonForm(forms.ModelForm):

  class Meta:
    model = Lesson
    fields = ['subject', 'group', 'teacher', 'date', 'start_time', 'end_time']
    widgets = {
        'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        'start_time': forms.TimeInput(
            attrs={'type': 'time', 'class': 'form-control'}
        ),
        'end_time': forms.TimeInput(
            attrs={'type': 'time', 'class': 'form-control'}
        ),
        'subject': forms.TextInput(attrs={'class': 'form-control'}),
        'group': forms.Select(attrs={'class': 'form-control'}),
        'teacher': forms.Select(attrs={'class': 'form-control'}),
    }

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.fields['teacher'].queryset = User.objects.filter(
        role=User.Role.TEACHER
    )


class AttendanceForm(forms.ModelForm):
  class Meta:
    model = Attendance
    fields = ['is_present']
    widgets = {
        'is_present': forms.CheckboxInput(
            attrs={'class': 'form-check-input'}
        ),
    }