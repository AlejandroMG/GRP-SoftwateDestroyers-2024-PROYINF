# Generated by Django 3.2.25 on 2024-10-16 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dicomViewer', '0004_alter_dicomfile_usuario'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dicomfile',
            name='dicom_file',
            field=models.BinaryField(),
        ),
    ]
