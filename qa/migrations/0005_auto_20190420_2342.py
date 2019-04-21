# Generated by Django 2.2 on 2019-04-21 02:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0004_resposta'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario', models.CharField(max_length=100, unique=True)),
                ('senha', models.CharField(max_length=25)),
            ],
        ),
        migrations.AlterField(
            model_name='resposta',
            name='texto',
            field=models.CharField(max_length=1001),
        ),
    ]
