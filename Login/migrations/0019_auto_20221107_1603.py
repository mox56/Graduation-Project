# Generated by Django 3.2.12 on 2022-11-07 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0018_department_course_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='department',
            name='course_id',
        ),
        migrations.AddField(
            model_name='department',
            name='department_id',
            field=models.IntegerField(null=True),
        ),
    ]