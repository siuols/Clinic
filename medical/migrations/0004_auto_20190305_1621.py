# Generated by Django 2.1.7 on 2019-03-05 16:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0003_auto_20190305_1620'),
    ]

    operations = [
        migrations.RenameField(
            model_name='history',
            old_name='medication',
            new_name='treatment',
        ),
    ]
