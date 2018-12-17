# Generated by Django 2.1.4 on 2018-12-06 21:44

from django.db import migrations, models
import simditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Index',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='标题')),
                ('img', models.ImageField(default='img/demo.jpg', upload_to='img', verbose_name='图片')),
                ('summary', simditor.fields.RichTextField(blank=True, null=True, verbose_name='项目介绍')),
            ],
            options={
                'verbose_name': '首页',
                'verbose_name_plural': '首页',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='LunBo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=50, null=True, verbose_name='标题 可为空')),
                ('img', models.ImageField(default='img/demo.jpg', upload_to='img', verbose_name='图片')),
            ],
            options={
                'verbose_name': '轮播图',
                'verbose_name_plural': '轮播图',
                'ordering': ['-id'],
            },
        ),
    ]