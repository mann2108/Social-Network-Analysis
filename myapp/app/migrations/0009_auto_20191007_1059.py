# Generated by Django 2.2.3 on 2019-10-07 05:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20191007_1052'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='dislikes',
            field=models.IntegerField(default=5158),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=4017),
        ),
    ]
