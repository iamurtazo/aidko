from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import views as auth_views, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.db.models import Q, Count
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.urls import reverse_lazy
from .models import Question, Answer, Category, Tag
from .forms import QuestionForm, AnswerForm


def home(request):
    """Home page with recent questions and categories"""
    recent_questions = Question.objects.select_related('author', 'category').prefetch_related('tags', 'upvotes').annotate(
        upvote_count=Count('upvotes'),
        answer_count=Count('answers')
    )[:6]  # Show only 6 recent questions on homepage
    
    categories = Category.objects.annotate(
        question_count=Count('questions')
    )
    
    # Get some stats for the homepage
    total_users = Question.objects.values('author').distinct().count()
    total_questions = Question.objects.count()
    total_answers = Answer.objects.count()
    
    context = {
        'recent_questions': recent_questions,
        'categories': categories,
        'total_users': total_users,
        'total_questions': total_questions,
        'total_answers': total_answers,
        'active_page': 'home'
    }
    return render(request, 'index.html', context)


def questions_list(request):
    """List all questions with filtering and search"""
    questions = Question.objects.select_related('author', 'category').prefetch_related('tags', 'upvotes').annotate(
        upvote_count=Count('upvotes'),
        answer_count=Count('answers')
    )
    
    # Search functionality
    search_query = request.GET.get('search')
    if search_query:
        questions = questions.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(tags__name__icontains=search_query)
        ).distinct()
    
    # Category filtering
    category_slug = request.GET.get('category')
    if category_slug:
        questions = questions.filter(category__slug=category_slug)
    
    # Sorting
    sort_by = request.GET.get('sort', 'recent')
    if sort_by == 'popular':
        questions = questions.order_by('-upvote_count', '-created_at')
    elif sort_by == 'answered':
        questions = questions.order_by('-answer_count', '-created_at')
    else:  # recent
        questions = questions.order_by('-created_at')
    
    categories = Category.objects.annotate(
        question_count=Count('questions')
    )
    
    context = {
        'questions': questions,
        'categories': categories,
        'search_query': search_query,
        'current_category': category_slug,
        'current_sort': sort_by,
        'active_page': 'questions'
    }
    return render(request, 'questions.html', context)


def question_detail(request, slug):
    """Question detail page with answers"""
    question = get_object_or_404(
        Question.objects.select_related('author', 'category').prefetch_related('tags', 'upvotes'),
        slug=slug
    )
    
    # Increment view count
    question.views += 1
    question.save(update_fields=['views'])
    
    answers = question.answers.select_related('author').prefetch_related('upvotes').annotate(
        upvote_count=Count('upvotes')
    )
    
    # Handle answer form submission
    if request.method == 'POST' and request.user.is_authenticated:
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()
            messages.success(request, 'Your answer has been posted!')
            return redirect('qa:question_detail', slug=slug)
    else:
        form = AnswerForm()
    
    context = {
        'question': question,
        'answers': answers,
        'form': form,
        'user_has_upvoted_question': request.user in question.upvotes.all() if request.user.is_authenticated else False,
    }
    return render(request, 'question_detail.html', context)


@login_required
def ask_question(request):
    """Ask a new question"""
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.author = request.user
            question.save()
            form.save_m2m()  # Save many-to-many relationships (tags)
            messages.success(request, 'Your question has been posted!')
            return redirect('qa:question_detail', slug=question.slug)
    else:
        form = QuestionForm()
    
    context = {
        'form': form,
        'active_page': 'ask_question'
    }
    return render(request, 'ask_question.html', context)


def category_questions(request, slug):
    """Questions in a specific category"""
    category = get_object_or_404(Category, slug=slug)
    questions = Question.objects.filter(category=category).select_related('author', 'category').prefetch_related('tags', 'upvotes').annotate(
        upvote_count=Count('upvotes'),
        answer_count=Count('answers')
    ).order_by('-created_at')
    
    context = {
        'category': category,
        'questions': questions,
        'active_page': 'questions'
    }
    return render(request, 'category_questions.html', context)


@login_required
@require_POST
def upvote_question(request, question_id):
    """AJAX endpoint to upvote/downvote a question"""
    question = get_object_or_404(Question, id=question_id)
    
    if request.user in question.upvotes.all():
        question.upvotes.remove(request.user)
        upvoted = False
    else:
        question.upvotes.add(request.user)
        upvoted = True
    
    return JsonResponse({
        'upvoted': upvoted,
        'upvote_count': question.upvote_count()
    })


@login_required
@require_POST
def upvote_answer(request, answer_id):
    """AJAX endpoint to upvote/downvote an answer"""
    answer = get_object_or_404(Answer, id=answer_id)
    
    if request.user in answer.upvotes.all():
        answer.upvotes.remove(request.user)
        upvoted = False
    else:
        answer.upvotes.add(request.user)
        upvoted = True
    
    return JsonResponse({
        'upvoted': upvoted,
        'upvote_count': answer.upvote_count()
    })


def community(request):
    """Community page"""
    context = {
        'active_page': 'community'
    }
    return render(request, 'community.html', context)


def blog(request):
    """Blog page"""
    context = {
        'active_page': 'blog'
    }
    return render(request, 'blog.html', context)


# Authentication Views
class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add CSS classes to form fields
        for field_name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})


def register_view(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Welcome to AidKo! Your account has been created.')
            return redirect('qa:home')
    else:
        form = CustomUserCreationForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)


class CustomLoginView(auth_views.LoginView):
    template_name = 'login.html'
    redirect_authenticated_user = True
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Add CSS classes to form fields
        for field_name, field in form.fields.items():
            field.widget.attrs.update({'class': 'form-control'})
        return form
    
    def form_valid(self, form):
        messages.success(self.request, f'Welcome back, {form.get_user().username}!')
        return super().form_valid(form)


class CustomLogoutView(auth_views.LogoutView):
    template_name = 'logout.html'
    next_page = '/logged-out/'
    
    def get(self, request, *args, **kwargs):
        # Show logout confirmation page
        return render(request, self.template_name)
    
    def post(self, request, *args, **kwargs):
        # Actually log out the user
        if request.user.is_authenticated:
            username = request.user.username
            messages.success(request, f'Goodbye, {username}! You have been logged out successfully.')
        # Call the parent post method to actually log out
        return super().post(request, *args, **kwargs)


def logged_out_view(request):
    """Custom logged out confirmation page"""
    return render(request, 'logged_out.html')
