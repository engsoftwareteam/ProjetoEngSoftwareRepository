# Generated by Django 2.2 on 2019-04-29 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0014_pergunta_titulo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pergunta',
            name='texto',
            field=models.TextField(default='texto default', max_length=10000),
        ),
        migrations.AlterField(
            model_name='resposta',
            name='texto',
            field=models.TextField(max_length=10000),
        ),
    ]