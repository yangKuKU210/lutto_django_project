# Generated by Django 2.1.1 on 2018-10-24 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0004_auto_20181021_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='addgood',
            name='num',
            field=models.IntegerField(default=0),
        ),
    ]
