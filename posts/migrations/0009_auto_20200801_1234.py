# Generated by Django 3.0.8 on 2020-08-01 02:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0008_auto_20200801_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='user_profile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='posts.UserProfile'),
        ),
    ]
