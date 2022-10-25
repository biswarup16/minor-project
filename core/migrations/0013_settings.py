# Generated by Django 4.1.1 on 2022-10-24 17:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Settings',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Name of the Institution')),
                ('logo', models.ImageField(blank=True, null=True, upload_to='Logo', verbose_name='Logo')),
                ('favicon', models.ImageField(blank=True, null=True, upload_to='Logo', verbose_name='Favicon')),
                ('address', models.TextField(blank=True, null=True, verbose_name='Address')),
                ('pin_code', models.CharField(blank=True, max_length=6, null=True, verbose_name='Pin Code')),
                ('phone1', models.CharField(blank=True, max_length=12, null=True, verbose_name='Contact Number 1')),
                ('phone2', models.CharField(blank=True, max_length=12, null=True, verbose_name='Contact Number 2')),
            ],
            options={
                'verbose_name': 'Setting',
                'verbose_name_plural': 'Settings',
            },
        ),
    ]