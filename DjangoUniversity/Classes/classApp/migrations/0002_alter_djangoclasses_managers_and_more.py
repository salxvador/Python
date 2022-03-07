# Generated by Django 4.0.3 on 2022-03-07 17:56

from django.db import migrations, models
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ('classApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='djangoclasses',
            managers=[
                ('object', django.db.models.manager.Manager()),
            ],
        ),
        migrations.AddField(
            model_name='djangoclasses',
            name='CourseNumber',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='djangoclasses',
            name='Duration',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10000),
        ),
        migrations.AddField(
            model_name='djangoclasses',
            name='InstructorName',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AddField(
            model_name='djangoclasses',
            name='Title',
            field=models.CharField(default='', max_length=40),
        ),
    ]
