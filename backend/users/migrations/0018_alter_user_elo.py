# Generated by Django 3.2.25 on 2024-06-12 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_user_is_verified'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='elo',
            field=models.IntegerField(default=0),
        ),
    ]
