# Generated by Django 2.0.5 on 2018-05-30 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('iot', '0002_auto_20180530_1850'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postmodel',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='iot/', verbose_name='Ảnh:'),
        ),
    ]