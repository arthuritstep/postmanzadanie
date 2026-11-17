from django.contrib.auth.models import AbstractUser
from django.db import models


class StudyGroup(models.Model):
  name = models.CharField(max_length=50, unique=True, verbose_name='Группа')

  def __str__(self):
    return self.name


class User(AbstractUser):

  class Role(models.TextChoices):
    MANAGER = 'manager', 'Менеджер'
    TEACHER = 'teacher', 'Преподаватель'
    STUDENT = 'student', 'Студент'

  role = models.CharField(
      max_length=20, choices=Role.choices, default=Role.STUDENT
  )
  group = models.ForeignKey(
      StudyGroup,
      on_delete=models.SET_NULL,
      null=True,
      blank=True,
      related_name='students',
      verbose_name='Учебная группа',
  )


class Lesson(models.Model):
  subject = models.CharField(max_length=200, verbose_name='Предмет')
  group = models.ForeignKey(
      StudyGroup,
      on_delete=models.CASCADE,
      related_name='lessons',
      verbose_name='Группа',
  )
  teacher = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      related_name='lessons',
      limit_choices_to={'role': 'teacher'},
      verbose_name='Преподаватель',
  )
  date = models.DateField(verbose_name='Дата')
  start_time = models.TimeField(verbose_name='Время начала')

  def __str__(self):
    return f'{self.subject} ({self.group.name}) - {self.date}'


class Attendance(models.Model):
  lesson = models.ForeignKey(
      Lesson,
      on_delete=models.CASCADE,
      related_name='attendances',
      verbose_name='Пара',
  )
  student = models.ForeignKey(
      User,
      on_delete=models.CASCADE,
      limit_choices_to={'role': 'student'},
      verbose_name='Студент',
  )
  is_present = models.BooleanField(
      default=True, verbose_name='Присутствует'
  )

  class Meta:
    unique_together = ('lesson', 'student')