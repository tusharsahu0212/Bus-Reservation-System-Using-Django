# Generated by Django 5.0.3 on 2024-03-24 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bus', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='email',
        ),
        migrations.AddField(
            model_name='booking',
            name='nos',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
