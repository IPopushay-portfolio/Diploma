# Generated by Django 5.2.3 on 2025-06-20 14:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("lm", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name="course",
            name="teacher",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="educationalmodule",
            name="author",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="educationalmodule",
            name="course",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, related_name="modules", to="lm.course"
            ),
        ),
        migrations.AddField(
            model_name="enrollment",
            name="module",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="lm.educationalmodule"),
        ),
        migrations.AddField(
            model_name="enrollment",
            name="student",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="material",
            name="uploaded_by",
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name="educationalmodule",
            name="materials",
            field=models.ManyToManyField(to="lm.material"),
        ),
        migrations.AlterUniqueTogether(
            name="educationalmodule",
            unique_together={("course", "order_number")},
        ),
    ]
