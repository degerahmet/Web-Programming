# Generated by Django 3.1 on 2020-08-22 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_product_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='owner',
            field=models.IntegerField(),
        ),
    ]
