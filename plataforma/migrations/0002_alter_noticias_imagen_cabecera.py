# Generated by Django 5.0.2 on 2024-06-25 13:29

import plataforma.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='noticias',
            name='imagen_cabecera',
            field=models.ImageField(blank=True, null=True, upload_to='Noticias/25-06-2024/', validators=[plataforma.models.validate_file_extension]),
        ),
    ]
