# Generated by Django 5.1.1 on 2024-11-21 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('extension', '0002_alter_email_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='perfil_laboral',
            name='hoja_de_vida',
            field=models.FileField(blank=True, null=True, upload_to='hojas_de_vida/'),
        ),
    ]
