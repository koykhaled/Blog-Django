# Generated by Django 4.2.7 on 2023-11-08 15:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0010_alter_post_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(default=datetime.datetime(2023, 11, 8, 15, 50, 35, 942098, tzinfo=datetime.timezone.utc)),
        ),
    ]
