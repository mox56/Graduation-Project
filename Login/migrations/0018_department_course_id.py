# Generated by Django 3.2.12 on 2022-11-07 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0017_auto_20221107_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='course_id',
            field=models.IntegerField(max_length=5, null=True),
        ),
    ]