from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Student, ContactMessage

BRANCHES = [("Btech", "Btech"), ("MCA", "MCA"), ("BCA", "BCA"), ("BE", "BE")]


class RegisterForm(UserCreationForm):
    full_name = forms.CharField(max_length=100)
    roll_number = forms.CharField(max_length=30)
    branch = forms.ChoiceField(choices=BRANCHES)
    cgpa = forms.DecimalField(
        max_digits=3, decimal_places=2, min_value=0, max_value=10)

    def clean_roll_number(self):
        roll = self.cleaned_data["roll_number"]
        if Student.objects.filter(roll_number=roll).exists():
            raise forms.ValidationError(
                "This roll number is already registered.")
        return roll

    def save(self, commit=True):
        user = super().save(commit)
        Student.objects.create(
            user=user,
            full_name=self.cleaned_data["full_name"],
            roll_number=self.cleaned_data["roll_number"],
            branch=self.cleaned_data["branch"],
            cgpa=self.cleaned_data["cgpa"],
        )
        return user


class ProfileForm(forms.ModelForm):
    branch = forms.ChoiceField(choices=BRANCHES)

    class Meta:
        model = Student
        fields = ["full_name", "phone", "branch",
                  "cgpa", "skills", "image", "resume"]

    def clean_resume(self):
        f = self.cleaned_data.get("resume")
        if f:
            if not f.name.lower().endswith(".pdf"):
                raise forms.ValidationError("Only PDF files are allowed.")
            if f.size > 2 * 1024 * 1024:
                raise forms.ValidationError("Resume must be under 2 MB.")
        return f

    def clean_image(self):
        f = self.cleaned_data.get("image")
        if f and f.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Photo must be under 2 MB.")
        return f


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "subject", "message"]
        widgets = {"message": forms.Textarea(attrs={"rows": 4})}
