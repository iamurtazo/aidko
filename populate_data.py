#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.contrib.auth.models import User
from qa.models import Category, Tag, Question, Answer

# Create categories
categories_data = [
    {'name': 'Housing', 'description': 'Questions about finding apartments, housing contracts, and living arrangements', 'icon': 'fas fa-building'},
    {'name': 'Documentation', 'description': 'Visa, ARC cards, work permits and other official documents', 'icon': 'fas fa-file-alt'},
    {'name': 'Banking', 'description': 'Opening bank accounts, money transfers, and financial services', 'icon': 'fas fa-university'},
    {'name': 'Healthcare', 'description': 'Health insurance, finding doctors, and medical services', 'icon': 'fas fa-heartbeat'},
    {'name': 'Language', 'description': 'Korean language learning, translation services, and communication', 'icon': 'fas fa-comments'},
    {'name': 'Local Life', 'description': 'Culture, customs, local services, and daily life tips', 'icon': 'fas fa-map-marker-alt'},
]

print("Creating categories...")
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={
            'description': cat_data['description'],
            'icon': cat_data['icon']
        }
    )
    if created:
        print(f"✓ Created category: {category.name}")

# Create sample users
print("\nCreating sample users...")
users_data = [
    {'username': 'john_expat', 'email': 'john@example.com', 'first_name': 'John', 'last_name': 'Smith'},
    {'username': 'sarah_korea', 'email': 'sarah@example.com', 'first_name': 'Sarah', 'last_name': 'Johnson'},
    {'username': 'mike_seoul', 'email': 'mike@example.com', 'first_name': 'Mike', 'last_name': 'Brown'},
]

for user_data in users_data:
    user, created = User.objects.get_or_create(
        username=user_data['username'],
        defaults={
            'email': user_data['email'],
            'first_name': user_data['first_name'],
            'last_name': user_data['last_name'],
            'password': 'pbkdf2_sha256$600000$xyz$abc123'  # dummy password
        }
    )
    if created:
        print(f"✓ Created user: {user.username}")

# Create sample questions
print("\nCreating sample questions...")
questions_data = [
    {
        'title': 'How to get an ARC card as a student in Seoul?',
        'description': 'I just arrived in Seoul for my exchange program and need to get my ARC card. What documents do I need and where should I go? How long does the process take?',
        'category': 'Documentation',
        'author': 'john_expat',
        'tags': ['arc-card', 'student', 'seoul', 'visa']
    },
    {
        'title': 'Best bank for foreigners in Korea?',
        'description': 'I need to open a bank account in Korea. Which banks are most foreigner-friendly? What documents do I need to bring?',
        'category': 'Banking',
        'author': 'sarah_korea',
        'tags': ['banking', 'account', 'foreigner']
    },
    {
        'title': 'How to find an apartment in Gangnam?',
        'description': 'Looking for a one-room apartment in Gangnam area. What websites should I use? Any tips for dealing with real estate agents?',
        'category': 'Housing',
        'author': 'mike_seoul',
        'tags': ['apartment', 'gangnam', 'housing', 'real-estate']
    },
    {
        'title': 'Korean health insurance for expats?',
        'description': 'Just started working in Korea. How does the national health insurance work? Do I need to register somewhere?',
        'category': 'Healthcare',
        'author': 'john_expat',
        'tags': ['health-insurance', 'expat', 'work']
    },
]

users = {user.username: user for user in User.objects.all()}
categories = {cat.name: cat for cat in Category.objects.all()}

for q_data in questions_data:
    author = users.get(q_data['author'])
    category = categories.get(q_data['category'])
    
    if author and category:
        question, created = Question.objects.get_or_create(
            title=q_data['title'],
            defaults={
                'description': q_data['description'],
                'author': author,
                'category': category,
            }
        )
        
        if created:
            # Add tags
            for tag_name in q_data['tags']:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                question.tags.add(tag)
            
            print(f"✓ Created question: {question.title[:50]}...")

# Create sample answers
print("\nCreating sample answers...")
answers_data = [
    {
        'question_title': 'How to get an ARC card as a student in Seoul?',
        'content': 'You need to go to the immigration office with your passport, visa, school enrollment certificate, and a passport photo. The process usually takes 1-2 weeks. Make sure to bring the exact fee in cash!',
        'author': 'sarah_korea'
    },
    {
        'question_title': 'Best bank for foreigners in Korea?',
        'content': 'I recommend KB Kookmin Bank or Shinhan Bank. They have English-speaking staff and good online banking. You\'ll need your ARC card, passport, and employment certificate.',
        'author': 'mike_seoul'
    },
]

questions_dict = {q.title: q for q in Question.objects.all()}

for a_data in answers_data:
    question = questions_dict.get(a_data['question_title'])
    author = users.get(a_data['author'])
    
    if question and author:
        answer, created = Answer.objects.get_or_create(
            question=question,
            author=author,
            defaults={'content': a_data['content']}
        )
        
        if created:
            print(f"✓ Created answer for: {question.title[:30]}...")

print(f"\n🎉 Sample data created successfully!")
print(f"📊 Created {Category.objects.count()} categories")
print(f"👥 Created {User.objects.count()} users")
print(f"❓ Created {Question.objects.count()} questions")
print(f"💬 Created {Answer.objects.count()} answers")
print(f"🏷️ Created {Tag.objects.count()} tags")
