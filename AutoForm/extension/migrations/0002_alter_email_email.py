# Generated by Django 4.2.16 on 2024-11-05 23:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extension', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='email',
            name='email',
            field=models.EmailField(max_length=100),
        ),
    ]
