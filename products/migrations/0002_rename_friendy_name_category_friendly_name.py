# Generated by Django 3.2 on 2022-04-16 14:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='category',
            old_name='friendy_name',
            new_name='friendly_name',
        ),
    ]
