# Generated by Django 3.2.10 on 2024-05-27 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_user_validation_code_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='elo',
            field=models.IntegerField(default=0),
        ),
    ]
