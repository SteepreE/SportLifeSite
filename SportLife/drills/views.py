import datetime

from django.http import HttpRequest

from . import database as db
from django.shortcuts import render, redirect
from .forms import UserRegistrationForm


def index(request: HttpRequest):
    return render(request, "new/index.html", context={'user_last_complex': db.get_active_user_complex(request.user)})


def registration(request: HttpRequest):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        pass_1 = request.POST.get("password1")
        pass_2 = request.POST.get("password2")
        
        bd_year = request.POST.get("birth_date_year")
        bd_month = request.POST.get("birth_date_month")
        bd_day = request.POST.get("birth_date_day")

        bd = f"{bd_year}-{bd_month}-{bd_day}"

        if pass_1 == pass_2:
            db.add_new_user(username, email, pass_1, bd)

            return redirect("/login/")

    return render(request, "new/registration.html", context={
        'user_last_complex': db.get_active_user_complex(request.user),
        'form': UserRegistrationForm
        }
    )


def profile(request: HttpRequest):

    user = request.user
    if not user.is_authenticated:
        return redirect("/")

    user_age = datetime.date.today() - user.birth_date

    last_complex = db.get_last_user_complex(user)
    user_active_complex = db.get_active_user_complex(user)

    context = {
        'user_nick': user.username,
        'user_name': user.get_full_name(),
        'user_mail': user.email,
        'user_bd': user.birth_date,
        'user_age': user_age.days // 360,
        'user_height': user.height,
        'user_weight': user.weight,
        'user_last_complex': user_active_complex,
        'user_active_complex': last_complex,
        'user_pass': user.password
    }

    return render(request, "new/profile.html", context=context)


def new_complex(request: HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect("/")

    if request.method == "POST":
        data = request.POST

        weight = float(data.get("weight"))
        purpose = db.get_pup(int(data.get("purpose")))

        height = float(data.get("height"))

        user.weight = weight
        user.height = height

        user.save()

        db.add_new_complex(user=user, purpose=purpose)

        return redirect("/select_drills/")

    return render(request, "new/new_complex.html",
                  context={'user_last_complex': db.get_active_user_complex(request.user)})


def select_drills(request: HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect("/")

    user_last_complex = db.get_active_user_complex(user)

    if request.method == "POST":
        data = request.POST

        drills_ids = data.getlist("drills")
        drills = []
        for drill_id in drills_ids:
            drill = db.get_drill(drill_id)
            drills.append(drill)

        db.add_drill_to_complex(user_last_complex, drills)

        return redirect("/user_drills/")

    complexes_drills = db.get_drills_for_complex(user_last_complex.purpose, db.get_user_weight_category(user))

    context = {
        "drills": complexes_drills,
        'user_last_complex': db.get_active_user_complex(request.user)
    }

    return render(request, "new/select_drills.html", context=context)


def profile_edit(request: HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect("/")

    user_complex = db.get_active_user_complex(user)

    if request.method == "POST":
        username = request.POST.get("username")

        bd_day = request.POST.get("bd_d")
        bd_month = request.POST.get("bd_m")
        bd_year = request.POST.get("bd_y")
        birth_date = f"{bd_year}-{bd_month}-{bd_day}"

        weight = float(request.POST.get("weight"))
        height = float(request.POST.get("height"))

        pass_1 = request.POST.get("password1")
        pass_2 = request.POST.get("password2")

        email = request.POST.get("email")

        user.username = username
        user.birth_date = birth_date
        user.weight = weight
        user.height = height
        user.email = email

        if pass_1 == pass_2 and pass_1 and pass_2:
            user.password = pass_1

        user.save()

        return redirect('/profile/')

    bd = str(user.birth_date).split('-')
    print(bd)

    context = {
        'bd_y': bd[0],
        'bd_m': bd[1],
        'bd_d': bd[2],
        'user_last_complex': user_complex
    }

    return render(request, "new/profile_edit.html", context=context)


def user_drills(request: HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect("/")

    user_complex = db.get_active_user_complex(user)
    drills = user_complex.drills.all()

    context = {
        'drills': drills,
        'user_last_complex': user_complex
    }

    return render(request, "new/user_drills.html", context=context)


def eff_test(request: HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect("/")

    user_complex = db.get_active_user_complex(user)

    if request.method == "POST":
        effectivity = request.POST.getlist("effectivity")

        for eff in effectivity:
            eff = str(eff).split("-")

            db.add_drill_effectivity(int(eff[0]), int(eff[1]))

        return redirect("/eff_result/")

    drills = db.get_last_user_complex(user).drills.all()

    context = {
        'drills': drills,
        'user_last_complex': user_complex
    }

    return render(request, "new/eff_test.html", context=context)


def eff_result(request: HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect("/")

    user_complex = db.get_active_user_complex(user)
    purposes = db.DrillPurpose.objects.all()

    if request.method == "POST":
        purpose_id = int(request.POST.get("purpose"))
        drills_eff = db.get_effectivity(purpose_id).items
        context = {
            'purposes': purposes,
            'drills_eff': drills_eff,
            'user_last_complex': user_complex
        }

        return render(request, "new/eff_result.html", context=context)

    context = {
        'drills_eff': None,
        'purposes': purposes,
        'user_last_complex': user_complex
    }

    return render(request, "new/eff_result.html", context=context)


def user_complexes(request: HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect("/")

    user_complex = db.get_active_user_complex(user)
    complexes = db.get_all_complexes_by_user(user)

    context = {
        'complexes': complexes,
        'user_last_complex': user_complex
    }

    return render(request, "new/user_complexes.html", context=context)


def end_complex(request: HttpRequest):
    user = request.user

    if not user.is_authenticated:
        return redirect("/")

    user_complex = db.get_active_user_complex(user)

    if request.method == "POST":
        duration = (datetime.date.today() - db.get_active_user_complex(user).start_date).days
        new_weight = int(request.POST.get('weight'))

        weight = user.weight - new_weight

        lost_weight = None
        get_weight = None

        if weight < 0:
            get_weight = abs(weight)
        else:
            lost_weight = abs(weight)

        favorite_drill = db.get_drill(request.POST.get('favorite_drill'))

        user_complex.favorite_drill = favorite_drill
        user_complex.weight_lost = lost_weight
        user_complex.duration = duration
        user_complex.is_active = False
        user_complex.save()

        user.weight = new_weight
        user.save()

        context = {
            'user_last_complex': user_complex,
            'duration': duration,
            'lost_weight': lost_weight,
            'get_weight': get_weight,
            'drill': favorite_drill
        }

        return render(request, "new/finish_complex.html", context=context)

    context = {
        'user_last_complex': user_complex,
        'complex_drills': user_complex.drills.all()
    }

    return render(request, "new/end_complex.html", context=context)




