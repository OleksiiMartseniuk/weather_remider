# Generated by Django 4.0.4 on 2022-05-18 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('weather', '0004_alter_subscriptioncity_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='city',
            name='name',
            field=models.CharField(max_length=20, unique=True, verbose_name='Название города'),
        ),
    ]
