# Generated by Django 2.1.1 on 2018-10-24 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0006_lovegood'),
    ]

    operations = [
        migrations.AddField(
            model_name='goodcomment',
            name='likes',
            field=models.IntegerField(default=0),
        ),
    ]
