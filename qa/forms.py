from django import forms
from .models import Question, Answer, Category, Tag


class QuestionForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text="Enter tags separated by commas (e.g., housing, seoul, apartment)",
        widget=forms.TextInput(attrs={
            'placeholder': 'housing, seoul, apartment',
            'class': 'form-control'
        })
    )
    
    class Meta:
        model = Question
        fields = ['title', 'description', 'category', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your question title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Provide more details about your question...'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            })
        }
    
    def save(self, commit=True):
        question = super().save(commit=commit)
        
        if commit:
            # Handle tags
            tags_input = self.cleaned_data.get('tags', '')
            if tags_input:
                tag_names = [name.strip() for name in tags_input.split(',') if name.strip()]
                for tag_name in tag_names:
                    tag, created = Tag.objects.get_or_create(name=tag_name.lower())
                    question.tags.add(tag)
        
        return question


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Write your answer here...'
            })
        }
