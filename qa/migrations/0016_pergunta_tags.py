# Generated by Django 2.2 on 2019-06-02 23:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0015_auto_20190428_2211'),
    ]

    operations = [
        migrations.AddField(
            model_name='pergunta',
            name='tags',
            field=models.TextField(null=True),
        ),
    ]
