from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import AbstractUser


class Drill(models.Model):
    name = models.CharField(max_length=50)

    description = models.TextField()

    purpose = models.ForeignKey('DrillPurpose', on_delete=models.SET_NULL, related_name='drills', null=True)
    weight_category = models.ForeignKey('WeightCategory', on_delete=models.SET_NULL, null=True)

    repeats_count = models.IntegerField()
    sets_count = models.IntegerField()

    def __str__(self):
        return self.name


class DrillPurpose(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class DrillEffectivity(models.Model):
    drill = models.ForeignKey('Drill', on_delete=models.CASCADE, related_name='effectivity')
    effectivity = models.IntegerField(validators=[MaxValueValidator(10), MinValueValidator(1)])


class WeightCategory(models.Model):
    name = models.CharField(max_length=50)

    min_weight = models.IntegerField()
    max_weight = models.IntegerField()

    def __str__(self):
        return self.name


class User(AbstractUser):
    birth_date = models.DateField(null=True)

    weight = models.FloatField(null=True)
    height = models.FloatField(null=True)


class DrillComplex(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='complexes')

    purpose = models.ForeignKey('DrillPurpose', on_delete=models.SET_NULL, null=True)

    duration = models.IntegerField(null=True)
    start_date = models.DateField(auto_now=True, null=True)

    is_active = models.BooleanField(default=True)

    weight_lost = models.FloatField(null=True)

    drills = models.ManyToManyField('Drill', related_name='complexes',  null=True)
    favorite_drill = models.ForeignKey('Drill', on_delete=models.SET_NULL, null=True)
