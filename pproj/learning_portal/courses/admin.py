from django.contrib import admin
from .models import Course, Quiz, Question, Option, Discussion, Comment, Resource

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at',)
    fields = ('title', 'description', 'instructors', 'students', 'youtube_url', 'youtube_playlist_url', 'created_at')
    readonly_fields = ('created_at',)

@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('course', 'created_at')

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'quiz', 'points')
    search_fields = ('text',)
    list_filter = ('quiz',)

@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct')
    search_fields = ('text',)
    list_filter = ('question', 'is_correct')

@admin.register(Discussion)
class DiscussionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'author', 'created_at')
    search_fields = ('title', 'content')
    list_filter = ('course', 'created_at')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'discussion', 'created_at')
    search_fields = ('content',)
    list_filter = ('created_at',)

@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'uploaded_by', 'upload_date', 'file')
    search_fields = ('title', 'description', 'file__icontains')
    list_filter = ('course', 'uploaded_by', 'upload_date')
    readonly_fields = ('uploaded_by', 'upload_date')
    # fields = ('course', 'title', 'description', 'file', 'uploaded_by') # Include uploaded_by for manual setting if needed

    def save_model(self, request, obj, form, change):
        # Automatically set the uploader to the current logged-in user when adding
        if not change:
            obj.uploaded_by = request.user
        obj.save()
