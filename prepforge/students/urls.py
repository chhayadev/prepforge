from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path("register/", views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("assessments/", views.assessments, name="assessments"),
    path("test/<str:category>/", views.take_test, name="take_test"),
    path("jobs/", views.jobs, name="jobs"),
    path("apply/<int:company_id>/", views.apply_job, name="apply_job"),
    path("profile/", views.profile, name="profile"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("contact/", views.contact, name="contact"),
]
