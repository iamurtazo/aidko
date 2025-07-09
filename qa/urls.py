from django.urls import path
from . import views

app_name = 'qa'

urlpatterns = [
    path('', views.home, name='home'),
    path('questions/', views.questions_list, name='questions'),
    path('questions/<slug:slug>/', views.question_detail, name='question_detail'),
    path('ask/', views.ask_question, name='ask_question'),
    path('category/<slug:slug>/', views.category_questions, name='category_questions'),
    path('community/', views.community, name='community'),
    path('blog/', views.blog, name='blog'),
    
    # Authentication URLs
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('logged-out/', views.logged_out_view, name='logged_out'),
    path('register/', views.register_view, name='register'),
    
    # AJAX endpoints
    path('upvote/question/<int:question_id>/', views.upvote_question, name='upvote_question'),
    path('upvote/answer/<int:answer_id>/', views.upvote_answer, name='upvote_answer'),
]
