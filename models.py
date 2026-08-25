from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    """One-to-one extension of Django's built-in User model."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student')
    name = models.CharField(max_length=150)
    email = models.EmailField()
    enrollment_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    instructor = models.CharField(max_length=100, blank=True)
    duration_weeks = models.PositiveIntegerField(default=6)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def total_topics(self):
        return Topic.objects.filter(module__course=self).count()

    def completed_topics_for(self, student):
        return StudentTopicProgress.objects.filter(
            topic__module__course=self, student=student, is_completed=True
        ).count()

    def progress_percent_for(self, student):
        total = self.total_topics()
        if total == 0:
            return 0
        return round((self.completed_topics_for(student) / total) * 100)


class Module(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='modules')
    module_number = models.PositiveIntegerField()
    title = models.CharField(max_length=150)

    class Meta:
        ordering = ['module_number']

    def __str__(self):
        return f"{self.course.name} - {self.title}"


class Topic(models.Model):
    module = models.ForeignKey(Module, on_delete=models.CASCADE, related_name='topics')
    topic_name = models.CharField(max_length=150)
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']

    def __str__(self):
        return self.topic_name


class StudentTopicProgress(models.Model):
    """
    Tracks per-student completion of a topic.

    Note: Topic.is_completed is kept as specified in the schema, but since
    Topic rows are shared course content (not duplicated per student), actual
    "mark as complete" state is tracked here per (student, topic) pair so
    that one student's progress never affects another student enrolled in
    the same course.
    """
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='topic_progress')
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='student_progress')
    is_completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('student', 'topic')

    def __str__(self):
        return f"{self.student.name} - {self.topic.topic_name} ({'done' if self.is_completed else 'pending'})"


class Enrollment(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('student', 'course')

    def __str__(self):
        return f"{self.student.name} -> {self.course.name}"
