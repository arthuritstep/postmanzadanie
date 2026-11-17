from rest_framework import serializers
from .models import Attendance, Lesson, StudyGroup, User


class StudyGroupSerializer(serializers.ModelSerializer):

  class Meta:
    model = StudyGroup
    fields = '__all__'


class LessonSerializer(serializers.ModelSerializer):

  class Meta:
    model = Lesson
    fields = '__all__'


class AttendanceSerializer(serializers.ModelSerializer):

  class Meta:
    model = Attendance
    fields = '__all__'