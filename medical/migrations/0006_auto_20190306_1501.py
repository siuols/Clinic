# Generated by Django 2.1.7 on 2019-03-06 15:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('medical', '0005_auto_20190306_0611'),
    ]

    operations = [
        migrations.AlterField(
            model_name='history',
            name='item_code',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='medical.Stock'),
        ),
        migrations.AlterField(
            model_name='history',
            name='quantity',
            field=models.IntegerField(),
        ),
    ]