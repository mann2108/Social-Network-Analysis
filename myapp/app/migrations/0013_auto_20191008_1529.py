# Generated by Django 2.2.3 on 2019-10-08 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0012_auto_20191007_1128'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='published_date',
        ),
        migrations.AddField(
            model_name='post',
            name='day',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='dislikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='tweeter',
            name='profile_pic_path',
            field=models.CharField(default='img.jpg', max_length=30),
        ),
    ]
