# Generated by Django 5.0 on 2024-01-08 13:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drills', '0006_alter_user_birth_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='drillcomplex',
            name='weight_lost',
            field=models.FloatField(null=True),
        ),
    ]
