# Generated by Django 4.1.7 on 2023-03-25 20:58

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0004_alter_examresult_student_index'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresult',
            name='Course_code',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Login.course'),
        ),
    ]
