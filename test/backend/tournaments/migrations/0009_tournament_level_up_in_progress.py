# Generated by Django 3.2.25 on 2024-07-18 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0008_alter_tournament_transaction_hashes'),
    ]

    operations = [
        migrations.AddField(
            model_name='tournament',
            name='level_up_in_progress',
            field=models.BooleanField(default=False),
        ),
    ]
