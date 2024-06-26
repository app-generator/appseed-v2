# Generated by Django 4.2.8 on 2024-06-05 05:41

from django.db import migrations, models
import django.db.models.deletion
import django_quill.fields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0029_alter_profile_role_alter_project_author_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='project',
        ),
        migrations.AddField(
            model_name='project',
            name='team',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='common.team'),
        ),
        migrations.AddField(
            model_name='team',
            name='description',
            field=django_quill.fields.QuillField(blank=True, null=True),
        ),
    ]
