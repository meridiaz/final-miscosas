# Generated by Django 3.0.3 on 2020-05-15 08:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('miscosas', '0010_remove_item_id_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='id_item',
            field=models.CharField(default='', max_length=20),
        ),
    ]