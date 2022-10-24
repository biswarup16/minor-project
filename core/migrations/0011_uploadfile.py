# Generated by Django 4.1.1 on 2022-10-14 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_admissiondocument'),
    ]

    operations = [
        migrations.CreateModel(
            name='UploadFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('document', models.FileField(upload_to='documents/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Upload File',
                'verbose_name_plural': 'Upload Files',
            },
        ),
    ]
