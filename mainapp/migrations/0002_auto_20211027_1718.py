# Generated by Django 3.2.8 on 2021-10-27 14:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='productcategory',
            name='slug',
        ),
    ]
