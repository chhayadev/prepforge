from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
from .models import Question, TestAttempt, Company, Application


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("dashboard")
    return render(request, "register.html", {"form": form})


# @login_required
# def dashboard(request):
#     student = request.user.student_profile
#     return render(request, "dashboard.html", {"student": student})

@login_required
def dashboard(request):
    s = request.user.student_profile
    readiness = s.readiness()
    apt = s.latest_score("aptitude")
    tech = s.latest_score("technical")

    if readiness >= 75:
        level, level_class = "Placement Ready", "bg-success"
    elif readiness >= 50:
        level, level_class = "Improving", "bg-warning text-dark"
    else:
        level, level_class = "Needs Work", "bg-danger"

    tips = []
    if not s.testattempt_set.filter(category="aptitude").exists():
        tips.append("Take the aptitude test")
    elif apt < 70:
        tips.append("Practice more aptitude questions (score below 70%)")
    if not s.testattempt_set.filter(category="technical").exists():
        tips.append("Take the technical test")
    elif tech < 70:
        tips.append("Revise core CS topics (score below 70%)")
    if len(s.skill_set()) < 3:
        tips.append("Add more skills to your profile")

    eligible_count = sum(1 for c in Company.objects.all() if c.is_eligible(s))

    return render(request, "dashboard.html", {
        "student": s,
        "readiness": readiness,
        "apt": apt,
        "tech": tech,
        "level": level,
        "level_class": level_class,
        "tips": tips,
        "eligible_count": eligible_count,
        "company_count": Company.objects.count(),
        "applications": s.application_set.select_related("company"),
    })


@login_required
def assessments(request):
    s = request.user.student_profile
    return render(request, "assessments.html", {
        "apt": s.latest_score("aptitude"),
        "tech": s.latest_score("technical"),
        "apt_count": Question.objects.filter(category="aptitude").count(),
        "tech_count": Question.objects.filter(category="technical").count(),
    })


@login_required
def take_test(request, category):
    if category not in ("aptitude", "technical"):
        return redirect("assessments")

    student = request.user.student_profile
    questions = list(Question.objects.filter(
        category=category).order_by("id")[:10])

    if request.method == "POST":
        total = len(questions)
        correct = sum(1 for q in questions if request.POST.get(
            f"q{q.id}") == q.correct)
        score = round(correct / total * 100) if total else 0
        TestAttempt.objects.create(
            student=student, category=category, score=score)
        return render(request, "result.html", {
            "score": score,
            "correct": correct,
            "total": total,
            "category": category,
            "readiness": student.readiness(),
        })

    return render(request, "take_test.html", {"questions": questions, "category": category})
