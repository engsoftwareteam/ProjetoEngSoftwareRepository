# Generated by Django 2.2 on 2019-06-02 21:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qa', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='VotosPerguntas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pergunta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.Pergunta')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='qa.Profile')),
            ],
        ),
    ]
