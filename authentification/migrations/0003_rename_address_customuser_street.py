# Generated by Django 4.2.3 on 2023-07-25 18:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0002_remove_customuser_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='address',
            new_name='street',
        ),
    ]
