# Generated by Django 3.2.12 on 2022-11-04 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0013_alter_department_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='index',
        ),
        migrations.AlterField(
            model_name='department',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(choices=[('Computer Science', 'Computer Science'), ('Information Technology', 'Information Technology')], max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]