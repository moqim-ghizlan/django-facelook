# Generated by Django 4.1.1 on 2022-11-30 22:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facelook', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.CharField(default='Pas encore de bio...', max_length=150),
        ),
    ]
