# Generated by Django 4.2.9 on 2024-01-10 15:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("projeekle", "0014_proje_users"),
    ]

    operations = [
        migrations.RemoveField(model_name="proje", name="group",),
        migrations.DeleteModel(name="Group",),
    ]
