# Generated by Django 4.0 on 2022-08-20 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='profile_pic',
            field=models.ImageField(default='default_profile.jpg', upload_to='profile'),
        ),
    ]