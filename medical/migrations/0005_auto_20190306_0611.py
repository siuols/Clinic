# Generated by Django 2.1.7 on 2019-03-06 06:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0004_auto_20190305_1621'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='treatment',
            new_name='medication',
        ),
    ]
