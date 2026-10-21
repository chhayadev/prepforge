from django.contrib import admin
from .models import Student, Question, TestAttempt, Company, Application


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "roll_number", "branch", "cgpa", "resume")
    search_fields = ("full_name", "roll_number")
    list_filter = ("branch",)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("text", "category", "correct")
    list_filter = ("category",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "ctc", "min_cgpa", "min_readiness")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("student", "company", "status",
                    "interview_date", "applied_on")
    list_filter = ("status", "company")
    list_editable = ("status", "interview_date")


admin.site.register(TestAttempt)
