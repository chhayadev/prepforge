from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Student, Company, TestAttempt, Application


class PrepForgeTests(TestCase):
    def setUp(self):
        u = User.objects.create_user("t1", password="pass12345")
        self.s = Student.objects.create(
            user=u, full_name="Test", roll_number="1",
            branch="Btech", cgpa=8, skills="Python, SQL")

    def test_readiness_formula(self):
        TestAttempt.objects.create(
            student=self.s, category="aptitude", score=80)
        TestAttempt.objects.create(
            student=self.s, category="technical", score=60)
        self.assertEqual(self.s.readiness(), 73)

    def test_eligible(self):
        c = Company.objects.create(name="A", role="Dev", ctc=5, min_cgpa=7,
                                   branches="Btech", required_skills="Python", min_readiness=0)
        self.assertTrue(c.is_eligible(self.s))

    def test_not_eligible_low_cgpa(self):
        c = Company.objects.create(name="B", role="Dev", ctc=5, min_cgpa=9,
                                   branches="Btech", required_skills="", min_readiness=0)
        self.assertFalse(c.is_eligible(self.s))

    def test_not_eligible_missing_skill(self):
        c = Company.objects.create(name="C", role="Dev", ctc=5, min_cgpa=7,
                                   branches="Btech", required_skills="Java", min_readiness=0)
        self.assertFalse(c.is_eligible(self.s))

    def test_duplicate_application_blocked(self):
        c = Company.objects.create(name="D", role="Dev", ctc=5, min_cgpa=7,
                                   branches="Btech", required_skills="", min_readiness=0)
        Application.objects.create(student=self.s, company=c)
        with self.assertRaises(Exception):
            Application.objects.create(student=self.s, company=c)

    def test_dashboard_needs_login(self):
        r = self.client.get(reverse("dashboard"))
        self.assertEqual(r.status_code, 302)
