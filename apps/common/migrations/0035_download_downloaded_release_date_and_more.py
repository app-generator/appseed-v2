# Generated by Django 4.2.8 on 2024-06-11 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0034_download'),
    ]

    operations = [
        migrations.AddField(
            model_name='download',
            name='downloaded_release_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='download',
            name='downloaded_version',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
