# Generated by Django 4.2.3 on 2023-08-28 20:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0017_alter_review_psychologist_alter_review_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='appointment',
            name='email',
            field=models.EmailField(default='example@example.com', max_length=254),
        ),
        migrations.AddField(
            model_name='appointment',
            name='full_name',
            field=models.CharField(default='John Doe', max_length=100),
        ),
    ]