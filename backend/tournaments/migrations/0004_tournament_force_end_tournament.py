# Generated by Django 3.2.25 on 2024-07-08 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0003_alter_tournament_level'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='force_end_tournament',
            field=models.IntegerField(default=0),
        ),
    ]
