# Generated by Django 2.2 on 2019-06-03 00:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0004_auto_20190602_2128'),
    ]

    operations = [
        migrations.RenameField(
            model_name='votosrespostas',
            old_name='pergunta',
            new_name='resposta',
        ),
    ]