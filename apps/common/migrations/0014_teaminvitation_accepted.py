# Generated by Django 4.2.8 on 2024-05-30 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0013_teaminvitation'),
    ]

    operations = [
        migrations.AddField(
            model_name='teaminvitation',
            name='accepted',
            field=models.BooleanField(default=False),
        ),
    ]
