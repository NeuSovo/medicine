# Generated by Django 2.1.2 on 2018-10-07 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('disease', '0007_auto_20181006_2255'),
    ]

    operations = [
        migrations.AddField(
            model_name='prescription',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='gif'),
        ),
    ]
