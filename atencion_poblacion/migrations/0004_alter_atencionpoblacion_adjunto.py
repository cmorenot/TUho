# Generated by Django 5.0.2 on 2024-06-27 19:23

import atencion_poblacion.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('atencion_poblacion', '0003_alter_atencionpoblacion_adjunto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atencionpoblacion',
            name='adjunto',
            field=models.FileField(blank=True, null=True, upload_to='AtencionPoblacion/27-06-2024/', validators=[atencion_poblacion.models.validate_file_extension]),
        ),
    ]
