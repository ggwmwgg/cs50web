# Generated by Django 4.2.2 on 2023-06-28 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('title_lower', models.CharField(max_length=64, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=64)),
                ('content', models.TextField(max_length=256)),
            ],
        ),
    ]
