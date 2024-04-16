# Generated by Django 4.2.7 on 2023-11-15 18:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("BookId", models.CharField(max_length=15, unique=True)),
                ("title", models.CharField(max_length=100)),
                ("author", models.CharField(max_length=50)),
            ],
        ),
    ]