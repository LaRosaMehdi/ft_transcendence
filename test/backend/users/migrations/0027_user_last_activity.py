# Generated by Django 3.2.25 on 2024-07-19 21:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0026_alter_user_is_superuser'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_activity',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
