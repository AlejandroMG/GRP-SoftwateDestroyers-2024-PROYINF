# Generated by Django 5.1.1 on 2024-11-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dicomViewer', '0006_estudio_dicomfile_estudio'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dicomfile',
            options={'ordering': ['instance_number']},
        ),
        migrations.AddField(
            model_name='dicomfile',
            name='instance_number',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
