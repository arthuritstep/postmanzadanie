from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Attendance, Lesson, StudyGroup
from .permissions import IsManager, IsTeacher
from .serializers import (
    AttendanceSerializer,
    LessonSerializer,
    StudyGroupSerializer,
)


class StudyGroupListCreateView(generics.ListCreateAPIView):
  queryset = StudyGroup.objects.all()
  serializer_class = StudyGroupSerializer
  permission_classes = [permissions.IsAuthenticated]


class LessonListCreateView(generics.ListCreateAPIView):
  serializer_class = LessonSerializer
  permission_classes = [permissions.IsAuthenticated]

  def get_queryset(self):
    user = self.request.user
    queryset = Lesson.objects.all()

    if user.role == 'teacher':
      queryset = queryset.filter(teacher=user)
    elif user.role == 'student' and user.group:
      queryset = queryset.filter(group=user.group)

    subject = self.request.query_params.get('subject')
    date = self.request.query_params.get('date')
    if subject:
      queryset = queryset.filter(subject__icontains=subject)
    if date:
      queryset = queryset.filter(date=date)

    return queryset

  def perform_create(self, serializer):
    if self.request.user.role != 'manager':
      from rest_framework.exceptions import PermissionDenied

      raise PermissionDenied('Только менеджер может создавать пары.')
    serializer.save()


class LessonRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
  queryset = Lesson.objects.all()
  serializer_class = LessonSerializer
  permission_classes = [permissions.IsAuthenticated, IsManager]


class MarkAttendanceView(APIView):
  permission_classes = [permissions.IsAuthenticated, IsTeacher]

  def post(self, request, lesson_id):
    try:
      lesson = Lesson.objects.get(id=lesson_id, teacher=request.user)
    except Lesson.DoesNotExist:
      return Response(
          {'error': 'Пара не найдена или принадлежит другому преподавателю.'},
          status=status.HTTP_403_FORBIDDEN,
      )

    student_id = request.data.get('student_id')
    is_present = request.data.get('is_present', True)

    attendance, created = Attendance.objects.update_or_create(
        lesson=lesson, student_id=student_id, defaults={'is_present': is_present}
    )

    return Response(
        {
            'status': 'Посещаемость успешно обновлена',
            'attendance_id': attendance.id,
        },
        status=status.HTTP_200_OK,
    )