# Generated by Django 4.1.7 on 2024-01-18 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0025_alter_examresult_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examresult',
            name='student_index',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Exam_result', to='Login.student'),
        ),
    ]