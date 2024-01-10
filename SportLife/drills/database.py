from django.db.models import QuerySet

from .models import *


def add_drill(name: str, description: str, purpose: DrillPurpose,
              weight_category: WeightCategory, repeats_count: int, sets_count: int) -> Drill:
    new_drill = Drill(
        name=name,
        description=description,
        purpose=purpose,
        weight_category=weight_category,
        repeats_count=repeats_count,
        sets_count=sets_count
    )
    new_drill.save()

    return new_drill


def get_user_weight_category(user: User):
    category = WeightCategory.objects.filter(
        min_weight__lt=user.weight,
        max_weight__gt=user.weight
    ).first()

    return category


def add_new_complex(user: User, purpose: DrillPurpose, duration=0) -> DrillComplex:
    new_complex = DrillComplex(
        user=user,
        purpose=purpose,
        duration=duration
    )

    new_complex.save()

    return new_complex


def add_drill_to_complex(new_complex: DrillComplex, drills: list[Drill]):
    for drill in drills:
        new_complex.drills.add(drill)


def get_drills_for_complex(purpose: DrillPurpose, user_weight_category: WeightCategory) -> list[Drill]:
    drills = purpose.drills.all()
    complex_drills = []

    for drill in list(drills):
        if drill.weight_category == user_weight_category:
            complex_drills.append(drill)

    return complex_drills


def get_all_complexes_by_user(user: User) -> QuerySet[DrillComplex]:
    complexes = user.complexes.all()

    return complexes


def get_active_user_complex(user: User) -> DrillComplex | None:
    if user.is_anonymous:
        return None

    last_complex = user.complexes.filter(
        is_active=True
    ).first()

    return last_complex


def get_last_user_complex(user: User) -> DrillComplex | None:
    if user.is_anonymous:
        return None

    last_complex = user.complexes.last()

    return last_complex


def add_new_user(username: str, email: str, password: str, birth_date: str) -> User:
    new_user = User.objects.create_user(
        username=username,
        email=email,
        birth_date=birth_date,
        password=password
    )

    new_user.save()

    return new_user


def add_drill_purpose(name: str) -> DrillPurpose:
    new_purpose = DrillPurpose(
        name=name
    )

    new_purpose.save()

    return new_purpose


def add_weight_category(name: str, min_weight: int, max_weight: int) -> WeightCategory:
    new_category = WeightCategory(
        name=name,
        min_weight=min_weight,
        max_weight=max_weight
    )

    new_category.save()

    return new_category


def get_user(key: int):
    return User.objects.get(pk=key)


def get_drill(key: int):
    return Drill.objects.get(pk=key)


def get_wc(key: int):
    return WeightCategory.objects.get(pk=key)


def get_pup(key: int):
    return DrillPurpose.objects.get(pk=key)


def get_complex(key: int):
    return DrillComplex.objects.get(pk=key)


def get_effectivity(purpose: int):
    drills = Drill.objects.filter(purpose=purpose).all()
    drills_effectivity = {}

    for drill in drills:

        e_drills = DrillEffectivity.objects.filter(drill=drill).all()

        eff = 0

        for e_drill in e_drills:
            eff += e_drill.effectivity
        if e_drills:
            drills_effectivity[drill.name] = round(eff / len(e_drills), 2)

    result = dict(sorted(drills_effectivity.items(), key=lambda item: item[1], reverse=True))

    return result


def add_drill_effectivity(drill_id: int, effectivity: int):
    drill = get_drill(drill_id)

    drill_effectivity = DrillEffectivity(
        drill=drill,
        effectivity=effectivity
    )

    drill_effectivity.save()

    return drill_effectivity
