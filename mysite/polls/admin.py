from django.contrib import admin

from .models import Choice, Question, Vote

class VoteAdmin(admin.ModelAdmin):
    fields = ['user', 'question', 'choice']
    list_display = ('user', 'question', 'choice')

class ChoiceAdmin(admin.ModelAdmin):
    fields = ['question', 'choice_text']
    list_display = ('question', 'choice_text', 'get_votes')

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 1

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(Vote, VoteAdmin)
