# AidKo - Q&A Community for Expats in Korea

AidKo is a Django-based Q&A community platform specifically designed to help expats living in Korea. It provides a space for asking questions, sharing knowledge, and connecting with experienced expats who can offer guidance on various aspects of life in Korea.

## 🌟 Features

### Core Q&A Functionality
- **Ask Questions**: Post questions with categories and tags
- **Answer System**: Provide detailed answers to community questions
- **Voting System**: Upvote helpful questions and answers
- **Search & Filter**: Find questions by keywords, categories, or tags
- **View Tracking**: Track how many times questions are viewed

### Community Features
- **User Authentication**: Register, login, and manage user profiles
- **Categories**: Organized topics (housing, language, culture, etc.)
- **Tags**: Flexible tagging system for better content organization
- **Community Stats**: Track community growth and engagement

### User Experience
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Modern UI**: Clean, intuitive interface with custom CSS styling
- **Navigation**: Easy-to-use navigation with active page highlighting
- **Real-time Updates**: AJAX-powered voting and interactions

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd aidko
   ```

2. **Create and activate virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run database migrations**
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Open your browser**
   Navigate to `http://127.0.0.1:8000/`

## 📁 Project Structure

```
aidko/
├── config/                 # Django project settings
│   ├── settings.py        # Main settings file
│   ├── urls.py           # Main URL configuration
│   └── wsgi.py           # WSGI configuration
├── qa/                    # Main app
│   ├── models.py         # Database models
│   ├── views.py          # View functions
│   ├── urls.py           # App URL patterns
│   ├── forms.py          # Form definitions
│   └── admin.py          # Admin interface
├── templates/             # HTML templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── questions.html    # Questions list
│   └── ...               # Other templates
├── static/               # Static files (CSS, JS, images)
│   ├── adinco_styles.css # Main styles
│   ├── questions_styles.css
│   └── images/           # Image assets
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## 🎯 Key Features Explained

### Question & Answer System
- Users can ask questions with titles, descriptions, and select categories
- Questions can be tagged for better organization
- Answers can be provided by community members
- Voting system helps identify the most helpful content

### Categories & Tags
- **Categories**: Broad topics like "Housing", "Language", "Culture", "Visa"
- **Tags**: Specific keywords for detailed categorization
- Both help users find relevant content quickly

### User Authentication
- Secure user registration and login
- User profiles with activity tracking
- Session management and logout functionality

### Search & Filtering
- Full-text search across questions and answers
- Filter by categories
- Sort by recent, popular, or most answered
- Combined search and filter functionality

## 🛠️ Technology Stack

- **Backend**: Django 5.1.3
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript (jQuery)
- **Styling**: Custom CSS with Font Awesome icons
- **Authentication**: Django's built-in auth system 