from django.db import models
from django.conf import settings


class Student(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="student_profile",
    )

    # Personal details
    full_name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=30, unique=True)
    phone = models.CharField(max_length=15, blank=True)
    image = models.ImageField(upload_to="students/", blank=True, null=True)
    resume = models.FileField(upload_to="resumes/", blank=True, null=True)

    # Academic details
    branch = models.CharField(max_length=10, default="CSE")
    cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=0)
    skills = models.CharField(
        max_length=200, blank=True, help_text="Comma separated, e.g. Python, SQL"
    )

    def __str__(self):
        return f"{self.full_name} ({self.roll_number})"

    def skill_set(self):
        return {s.strip().lower() for s in self.skills.split(",") if s.strip()}

    def latest_score(self, category):
        attempt = self.testattempt_set.filter(
            category=category).order_by("-date").first()
        return attempt.score if attempt else 0

    def readiness(self):
        return round(
            0.30 * float(self.cgpa) * 10
            + 0.35 * self.latest_score("aptitude")
            + 0.35 * self.latest_score("technical")
        )

    def is_placed(self):
        return self.application_set.filter(status="Selected").exists()


class Question(models.Model):
    CATEGORY = [("aptitude", "Aptitude"), ("technical", "Technical")]
    ANSWERS = [("a", "A"), ("b", "B"), ("c", "C"), ("d", "D")]

    category = models.CharField(max_length=10, choices=CATEGORY)
    text = models.CharField(max_length=300)
    option_a = models.CharField(max_length=150)
    option_b = models.CharField(max_length=150)
    option_c = models.CharField(max_length=150)
    option_d = models.CharField(max_length=150)
    correct = models.CharField(max_length=1, choices=ANSWERS)

    def __str__(self):
        return f"[{self.category}] {self.text}"


class TestAttempt(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    category = models.CharField(max_length=10)
    score = models.IntegerField(help_text="Percentage")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.category} - {self.score}%"


class Company(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    ctc = models.DecimalField(max_digits=5, decimal_places=2, help_text="LPA")
    min_cgpa = models.DecimalField(max_digits=3, decimal_places=2, default=6)
    branches = models.CharField(
        max_length=100, help_text="Comma separated, e.g. CSE,IT")
    required_skills = models.CharField(
        max_length=200, blank=True, help_text="Comma separated"
    )
    min_readiness = models.IntegerField(default=50)

    def __str__(self):
        return f"{self.name} - {self.role}"

    def is_eligible(self, s):
        need = {k.strip().lower()
                for k in self.required_skills.split(",") if k.strip()}
        allowed = [b.strip() for b in self.branches.split(",")]
        return (
            s.cgpa >= self.min_cgpa
            and s.branch in allowed
            and need <= s.skill_set()
            and s.readiness() >= self.min_readiness
        )


class Application(models.Model):
    STATUS = [(x, x) for x in ["Applied", "Shortlisted",
                               "Interview", "Selected", "Rejected"]]

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    status = models.CharField(max_length=12, choices=STATUS, default="Applied")
    applied_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("student", "company")

    def __str__(self):
        return f"{self.student.full_name} -> {self.company.name} ({self.status})"
