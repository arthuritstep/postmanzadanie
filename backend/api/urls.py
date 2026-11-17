from django.urls import path
from .views import (
    LessonListCreateView,
    LessonRetrieveUpdateDestroyView,
    MarkAttendanceView,
    StudyGroupListCreateView,
)

urlpatterns = [
    path('groups/', StudyGroupListCreateView.as_view(), name='group-list-create'),
    path('lessons/', LessonListCreateView.as_view(), name='lesson-list-create'),
    path(
        'lessons/<int:pk>/',
        LessonRetrieveUpdateDestroyView.as_view(),
        name='lesson-detail',
    ),
    path(
        'lessons/<int:lesson_id>/mark-attendance/',
        MarkAttendanceView.as_view(),
        name='mark-attendance',
    ),
]