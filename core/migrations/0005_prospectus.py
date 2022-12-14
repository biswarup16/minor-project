# Generated by Django 4.0 on 2022-09-18 18:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_profile_profile_pic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prospectus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, default=' ', max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, default=' ', max_length=50, null=True)),
                ('email', models.CharField(default=' ', max_length=50)),
                ('phone', models.CharField(blank=True, default=' ', max_length=12, null=True)),
                ('order_id', models.CharField(blank=True, default=' ', max_length=100, null=True)),
                ('razorpay_payment_id', models.CharField(blank=True, max_length=100)),
                ('paid', models.CharField(default=False, max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.profile')),
            ],
        ),
    ]
