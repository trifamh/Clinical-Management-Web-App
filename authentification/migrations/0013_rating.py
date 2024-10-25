# Generated by Django 4.2.3 on 2023-08-24 17:15

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentification', '0012_psychologist'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating_value', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('psychologist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='authentification.psychologist')),
            ],
        ),
    ]
