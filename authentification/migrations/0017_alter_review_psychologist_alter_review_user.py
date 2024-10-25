# Generated by Django 4.2.3 on 2023-08-28 15:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0016_review_delete_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='psychologist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='authentification.psychologist'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
