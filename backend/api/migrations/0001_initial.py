# Generated by Django 4.1.2 on 2022-11-30 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('department_code', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='CPUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_id', models.IntegerField()),
                ('major_type', models.BooleanField()),
                ('major', models.CharField(max_length=5)),
                ('minor', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Lecture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year', models.IntegerField()),
                ('semester', models.IntegerField()),
                ('num_classes', models.IntegerField()),
                ('num_labs', models.IntegerField()),
                ('credit', models.IntegerField()),
                ('credit_au', models.IntegerField()),
                ('course_rev_tot', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='LectureList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lectures', models.ManyToManyField(to='api.lecture')),
            ],
        ),
        migrations.CreateModel(
            name='Professor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('prof_id', models.IntegerField()),
                ('review_total_weigth', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Timeslot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.IntegerField()),
                ('begin', models.IntegerField()),
                ('end', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Schedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_saved', models.BooleanField()),
                ('lecture_list', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.lecturelist')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.cpuser')),
            ],
        ),
        migrations.AddField(
            model_name='lecture',
            name='classtime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='classtime', to='api.timeslot'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.course'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='examtime',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='examtime', to='api.timeslot'),
        ),
        migrations.AddField(
            model_name='lecture',
            name='professor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.professor'),
        ),
        migrations.AddField(
            model_name='cpuser',
            name='lecture_list',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.lecturelist'),
        ),
    ]