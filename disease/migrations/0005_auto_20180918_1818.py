# Generated by Django 2.1.1 on 2018-09-18 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disease', '0004_auto_20180918_1432'),
    ]

    operations = [
        migrations.AlterField(
            model_name='case',
            name='create_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
    ]