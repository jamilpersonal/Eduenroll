from django.contrib import admin
from .models import Student, Course, Module, Topic, Enrollment, StudentTopicProgress


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1


class ModuleInline(admin.TabularInline):
    model = Module
    extra = 1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'instructor', 'duration_weeks')
    search_fields = ('name',)
    inlines = [ModuleInline]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'module_number')
    list_filter = ('course',)
    inlines = [TopicInline]


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ('topic_name', 'module', 'is_completed')
    list_filter = ('module__course',)


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user', 'enrollment_date')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course', 'enrollment_date')
    list_filter = ('course',)


@admin.register(StudentTopicProgress)
class StudentTopicProgressAdmin(admin.ModelAdmin):
    list_display = ('student', 'topic', 'is_completed')
    list_filter = ('is_completed',)
