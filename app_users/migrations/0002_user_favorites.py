# Generated by Django 3.1.3 on 2020-12-08 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0001_initial'),
        ('app_users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='favorites',
            field=models.ManyToManyField(to='app_products.FoodProduct'),
        ),
    ]