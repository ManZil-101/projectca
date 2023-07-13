# Generated by Django 4.2.2 on 2023-07-13 04:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_alter_incidentinfo_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='incidentinfo',
            name='location',
        ),
        migrations.CreateModel(
            name='Incidentlocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('longitude', models.FloatField()),
                ('latitude', models.FloatField()),
                ('incident', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='home.incidentinfo')),
            ],
        ),
    ]