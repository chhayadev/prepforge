# PrepForge: Student Placement Readiness and Tracking System

PrepForge is a Django web application that helps students prepare for campus
placements and helps the placement cell manage and monitor the process.

## Features

**Student**

- Register, login and manage profile (photo, PDF resume, branch, CGPA, skills)
- Aptitude and technical tests with automatic scoring
- Readiness score (30% CGPA + 35% aptitude + 35% technical)
- Eligible / not eligible companies with reasons, and one-click apply
- Track application status and interview date

**Administrator**

- Manage students, questions, companies and eligibility criteria
- Admin overview page with placement statistics
- Shortlist candidates, set interview date and update placement status

## Tech Stack

Python, Django, SQLite, HTML, CSS, Bootstrap

## Setup

    python -m venv env
    source env/Scripts/activate        (Windows Git Bash)
    pip install -r requirements.txt
    python manage.py migrate
    python manage.py seed              (adds sample questions and companies)
    python manage.py createsuperuser
    python manage.py runserver

Open http://127.0.0.1:8000

## Pages

- Home: /
- Student register / login: /register/ , /login/
- Student dashboard: /dashboard/
- Admin overview: /admin-dashboard/
- Django admin: /admin/

## Run tests

    python manage.py test

## Author

[Your Name] - [Registration Number]
Master of Computer Application, Lovely Professional University
