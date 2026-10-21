

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, ProfileForm
# from .models import Question, TestAttempt, Company, Application
from .models import Student, Question, TestAttempt, Company, Application
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count


def get_student(request):
    return getattr(request.user, "student_profile", None)


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


def eligibility_reasons(company, s):
    reasons = []
    if s.cgpa < company.min_cgpa:
        reasons.append(f"CGPA below {company.min_cgpa}")
    if s.branch not in [b.strip() for b in company.branches.split(",")]:
        reasons.append("Branch not allowed")
    need = {k.strip().lower()
            for k in company.required_skills.split(",") if k.strip()}
    missing = need - s.skill_set()
    if missing:
        reasons.append("Missing skills: " + ", ".join(sorted(missing)))
    if s.readiness() < company.min_readiness:
        reasons.append(f"Readiness below {company.min_readiness}%")
    return reasons


@login_required
def jobs(request):
    s = request.user.student_profile
    applied = {a.company_id: a.status for a in s.application_set.all()}
    rows = []
    for c in Company.objects.all():
        reasons = eligibility_reasons(c, s)
        rows.append({
            "company": c,
            "eligible": not reasons,
            "reasons": reasons,
            "status": applied.get(c.id),
        })
    return render(request, "jobs.html", {"rows": rows, "readiness": s.readiness()})


@login_required
def apply_job(request, company_id):
    if request.method == "POST":
        s = request.user.student_profile
        company = get_object_or_404(Company, id=company_id)
        if company.is_eligible(s):
            _, created = Application.objects.get_or_create(
                student=s, company=company)
            if created:
                messages.success(request, f"Applied to {company.name}.")
            else:
                messages.info(request, "You have already applied.")
        else:
            messages.error(request, "You are not eligible for this company.")
    return redirect("jobs")


@login_required
def profile(request):
    s = request.user.student_profile
    form = ProfileForm(request.POST or None, request.FILES or None, instance=s)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profile updated.")
        return redirect("profile")
    return render(request, "profile.html", {"form": form})


STAGES = ["Applied", "Shortlisted", "Interview", "Selected", "Rejected"]


@staff_member_required
def admin_dashboard(request):
    if request.method == "POST":
        app = get_object_or_404(Application, id=request.POST.get("app_id"))
        status = request.POST.get("status")
        if status in STAGES:
            app.status = status
            app.save()
            messages.success(
                request, f"{app.student.full_name}: status changed to {status}.")
        return redirect("admin_dashboard")

    students = list(Student.objects.all())
    total_students = len(students)
    total_apps = Application.objects.count()
    placed = Student.objects.filter(
        application__status="Selected").distinct().count()

    stage_rows = []
    for st in STAGES:
        n = Application.objects.filter(status=st).count()
        stage_rows.append({"name": st, "count": n, "pct": round(
            n / total_apps * 100) if total_apps else 0})

    top_students = sorted(
        students, key=lambda s: s.readiness(), reverse=True)[:5]
    top = [{"student": s, "readiness": s.readiness()} for s in top_students]

    return render(request, "admin_dashboard.html", {
        "total_students": total_students,
        "ready": sum(1 for s in students if s.readiness() >= 75),
        "placed": placed,
        "placement_rate": round(placed / total_students * 100) if total_students else 0,
        "total_companies": Company.objects.count(),
        "total_apps": total_apps,
        "stage_rows": stage_rows,
        "stages": STAGES,
        "top": top,
        "companies": Company.objects.annotate(n=Count("application")).order_by("-n"),
        "applications": Application.objects.select_related("student", "company").order_by("-applied_on"),
    })
