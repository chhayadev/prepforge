from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    roll_number = forms.CharField(max_length=30)
    branch = forms.ChoiceField(
        choices=[("CSE", "CSE"), ("IT", "IT"), ("ECE", "ECE"), ("ME", "ME")])
    cgpa = forms.DecimalField(
        max_digits=3, decimal_places=2, min_value=0, max_value=10)

    def clean_roll_number(self):
        roll = self.cleaned_data["roll_number"]
        if Student.objects.filter(roll_number=roll).exists():
            raise forms.ValidationError(
                "This roll number is already registered.")
        return roll

    def save(self, commit=True):
        user = super().save(commit)          # 1. User banta hai (username + password)
        Student.objects.create(               # 2. Student profile banti hai
            user=user,
            full_name=self.cleaned_data["full_name"],
            roll_number=self.cleaned_data["roll_number"],
            branch=self.cleaned_data["branch"],
            cgpa=self.cleaned_data["cgpa"],
        )
        return user
