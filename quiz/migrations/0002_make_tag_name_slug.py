# Generated by Django 2.0 on 2017-12-11 08:53

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('quiz', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='name',
            field=models.SlugField(max_length=16, primary_key=True, serialize=False),
        ),
    ]