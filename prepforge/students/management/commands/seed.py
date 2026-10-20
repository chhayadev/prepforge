from django.core.management.base import BaseCommand
from students.models import Question, Company

APTITUDE = [
    ("If 20% of x is 40, then x = ?", "100", "200", "160", "80", "b"),
    ("Next number in the series: 2, 6, 12, 20, ?", "28", "30", "32", "26", "b"),
    ("A train 120 m long crosses a pole in 6 seconds. Its speed is?",
     "20 m/s", "24 m/s", "18 m/s", "12 m/s", "a"),
    ("Two numbers are in the ratio 3:5 and their sum is 64. The larger number is?",
     "24", "32", "40", "36", "c"),
    ("An item costs 80. Selling at 20% profit, the selling price is?",
     "96", "100", "90", "92", "a"),
    ("Average of 10, 20, 30, 40, 50 is?", "25", "30", "35", "40", "b"),
    ("A can do a work in 10 days and B in 15 days. Together they finish it in?",
     "5 days", "6 days", "7 days", "8 days", "b"),
    ("Simple interest on 1000 at 10% per year for 2 years is?",
     "100", "200", "210", "150", "b"),
    ("15% of 200 is?", "20", "25", "30", "35", "c"),
    ("Next number in the series: 5, 10, 20, 40, ?", "60", "70", "80", "100", "c"),
]

TECHNICAL = [
    ("Time complexity of binary search is?",
     "O(n)", "O(log n)", "O(n log n)", "O(1)", "b"),
    ("Which data structure follows LIFO?", "Queue", "Stack", "Heap", "Graph", "b"),
    ("Which SQL clause is used to filter groups?",
     "WHERE", "GROUP BY", "HAVING", "ORDER BY", "c"),
    ("Which of these is NOT a pillar of OOP?", "Inheritance",
     "Polymorphism", "Compilation", "Encapsulation", "c"),
    ("HTTP status code for 'Not Found' is?", "200", "301", "500", "404", "d"),
    ("Django is written in which language?", "Java", "Python", "PHP", "Ruby", "b"),
    ("What does a primary key do?", "Uniquely identifies each record",
     "Stores images", "Allows duplicate rows", "Joins two tables", "a"),
    ("HTML stands for?", "HyperText Markup Language", "High Text Machine Language",
     "Hyper Tool Multi Language", "Home Text Markup Language", "a"),
    ("Which of these is a relational database?",
     "MongoDB", "SQLite", "Redis", "Neo4j", "b"),
    ("Which data structure follows FIFO?", "Stack", "Queue", "Tree", "Array", "b"),
]

COMPANIES = [
    ("TechNova", "Software Engineer", 12, 8.0, "CSE,IT", "Python", 70),
    ("DataWise", "Data Analyst", 8, 7.0, "CSE,IT,ECE", "SQL", 50),
    ("StartupHub", "Associate Developer", 6, 6.5, "CSE,IT,ECE,ME", "", 40),
]


class Command(BaseCommand):
    help = "Adds sample questions and companies"

    def handle(self, *args, **kwargs):
        if Question.objects.count() == 0:
            for category, rows in (("aptitude", APTITUDE), ("technical", TECHNICAL)):
                for text, a, b, c, d, correct in rows:
                    Question.objects.create(
                        category=category, text=text,
                        option_a=a, option_b=b, option_c=c, option_d=d, correct=correct,
                    )
            self.stdout.write("20 questions added.")
        else:
            self.stdout.write("Questions already exist, skipped.")

        if Company.objects.count() == 0:
            for name, role, ctc, cgpa, branches, skills, ready in COMPANIES:
                Company.objects.create(
                    name=name, role=role, ctc=ctc, min_cgpa=cgpa,
                    branches=branches, required_skills=skills, min_readiness=ready,
                )
            self.stdout.write("3 companies added.")
        else:
            self.stdout.write("Companies already exist, skipped.")
