# Generated by Django 3.0.2 on 2020-04-25 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('testing', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accounts',
            name='Phone_Num',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]