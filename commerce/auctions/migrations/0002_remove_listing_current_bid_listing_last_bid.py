# Generated by Django 4.1.4 on 2023-01-15 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='current_bid',
        ),
        migrations.AddField(
            model_name='listing',
            name='last_bid',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
