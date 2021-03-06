# Generated by Django 2.1.2 on 2018-10-06 17:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('disease', '0002_auto_20181005_1547'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='casetyping',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='casetyping',
            name='case',
        ),
        migrations.RemoveField(
            model_name='casetyping',
            name='typing',
        ),
        migrations.RemoveField(
            model_name='diseasetypingsymptoms',
            name='symptoms_typing',
        ),
        migrations.AddField(
            model_name='case',
            name='case_typing',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='disease.DiseaseTyping'),
        ),
        migrations.AddField(
            model_name='diseasetyping',
            name='typing_symptoms',
            field=models.ManyToManyField(to='disease.DiseaseTypingSymptoms', verbose_name='分型症状'),
        ),
        migrations.DeleteModel(
            name='CaseTyping',
        ),
    ]
