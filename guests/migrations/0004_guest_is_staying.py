# Generated by Django 4.0.5 on 2022-07-15 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guests', '0003_remove_invitation_invitation_accepted_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='guest',
            name='is_staying',
            field=models.BooleanField(default=True),
        ),
    ]
