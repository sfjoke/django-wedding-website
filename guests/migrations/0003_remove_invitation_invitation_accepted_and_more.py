# Generated by Django 4.0.4 on 2022-05-16 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0002_guest_vegetarian_option_selected'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='invitation',
            name='invitation_accepted',
        ),
        migrations.RemoveField(
            model_name='invitation',
            name='invitation_text',
        ),
    ]
