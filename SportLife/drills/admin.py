from django.contrib import admin

from .models import Drill, DrillPurpose, WeightCategory

admin.site.register(Drill)
admin.site.register(DrillPurpose)
admin.site.register(WeightCategory)
