# Generated by Django 3.0.8 on 2020-07-24 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0002_auto_20200724_2225'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='posts.Tag'),
        ),
    ]