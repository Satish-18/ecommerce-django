# Generated by Django 3.0.6 on 2020-06-04 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_orders_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='phone',
            field=models.CharField(default=0, max_length=111),
        ),
    ]
