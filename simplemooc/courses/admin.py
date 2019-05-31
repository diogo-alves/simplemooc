from django.contrib import admin

from .models import Announcement, Comment, Course, Enrollment, Lesson, Material


class CourseAdmin(admin.ModelAdmin):

    list_display = ['name', 'slug', 'start_date', 'created_at']
    search_fields = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


class CommentAdmin(admin.ModelAdmin):

    list_display = ['announcement', 'user', 'comment', 'updated_at']
    search_fields = ['announcement__title', 'user__name', 'comment']


class MaterialInlineAdmin(admin.StackedInline):

    model = Material
    extra = 2


class LessonAdmin(admin.ModelAdmin):

    list_display = ['course', 'name', 'number', 'release_date']
    search_fields = ['course__name', 'name', 'description']
    list_filter = ['created_at', 'course__name']

    inlines = [MaterialInlineAdmin]


admin.site.register([Enrollment, Announcement, Material])
admin.site.register(Course, CourseAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Lesson, LessonAdmin)
