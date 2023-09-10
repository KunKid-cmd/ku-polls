from django.contrib import admin

from .models import Choice, Question


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date', 'end_date'],
                              'classes': ['collapse']}), ]
    inlines = [ChoiceInline]
    list_filter = ['pub_date', 'end_date']
    search_fields = ['question_text']
    list_display = ('question_text', 'pub_date', 'end_date', 'can_vote')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)