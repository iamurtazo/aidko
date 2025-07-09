from django.contrib import admin
from .models import Category, Tag, Question, Answer


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'question_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'question_count', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'upvote_count', 'answer_count', 'views', 'created_at']
    list_filter = ['category', 'created_at']
    search_fields = ['title', 'description', 'author__username']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags', 'upvotes']
    readonly_fields = ['views', 'created_at', 'updated_at']


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['question', 'author', 'upvote_count', 'is_accepted', 'created_at']
    list_filter = ['is_accepted', 'created_at']
    search_fields = ['content', 'author__username', 'question__title']
    filter_horizontal = ['upvotes']
    readonly_fields = ['created_at', 'updated_at']
