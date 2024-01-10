from django.urls import path, include
from . import views

from django.contrib.auth import views as av
from .forms import UserLoginForm

urlpatterns = [
    path("", views.index, name="index"),
    path("profile/", views.profile, name="profile"),
    path("new_complex/", views.new_complex, name="new_complex"),
    path("select_drills/", views.select_drills, name="new_complex"),
    path("end_complex/", views.end_complex, name="end_complex"),
    path("complexes/", views.user_complexes, name="complexes"),
    path("profile_edit/", views.profile_edit, name="complexes"),
    path("user_drills/", views.user_drills, name="profile"),
    path("eff_result/", views.eff_result, name="eff_result"),
    path("eff_test/", views.eff_test, name="eff_test"),
    path("login/", av.LoginView.as_view(template_name="login.html", authentication_form=UserLoginForm)),
    path("registration/", views.registration, name="registration"),
    path("", include("django.contrib.auth.urls"))
]
