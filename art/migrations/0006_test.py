# Generated by Django 4.0.2 on 2023-05-28 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('art', '0005_otp'),
    ]

    operations = [
        migrations.CreateModel(
            name='Test',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f', models.CharField(max_length=10)),
            ],
        ),
    ]
